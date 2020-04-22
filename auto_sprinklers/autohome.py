#!/usr/bin/python3
'''daemon for controling home 
gets data from sensors/schedule/etc.. and control the GPIOs'''
import time
from datetime import datetime
import argparse
import logging
import os
import sys
import daemon
from daemon import pidfile
import signal
import threading
import RPi.GPIO as GPIO
import django

script_path = os.path.dirname(__file__)
os.environ['DJANGO_SETTINGS_MODULE']='home.settings'
django.setup()

from sprinklers.models import Sprinkler, Sensor, Scheduler, Code
from sprinklers.views import read_gpio, write_gpio, lock_gpio, check_code

def check_if_other_sprinklers_on(gpio):
    ''' return True if any other sprinkler is on, False otherwise '''
    on = False
    if gpio:
        list_sprinklers = Sprinkler.objects.order_by('sprinkler_gpio')
        for sprinkler in list_sprinklers: 
            if sprinkler.sprinkler_gpio != gpio:
                check_gpio=read_gpio(sprinkler.sprinkler_gpio,'GPIO.OUT')
                if check_gpio != 'HIGH':
                    on = True
                    break
    return on

def stop_all_other_sprinklers(gpio,logger):
    ''' if gpio=0 stop all, else all others '''
    list_sprinklers = Sprinkler.objects.order_by('sprinkler_gpio')
    for sprinkler in list_sprinklers:
        if sprinkler.sprinkler_gpio != gpio:
            write_gpio(sprinkler.sprinkler_gpio, 1)
            lock_gpio(sprinkler.sprinkler_gpio, False)
            logger.info('Sensor GPIO %d is set to HIGH and unlocked', sprinkler.sprinkler_gpio)

def stop_all_locked_sprinklers(logger):
    ''' if gpio=0 stop all, else all others '''
    list_sprinklers = Sprinkler.objects.order_by('sprinkler_gpio')
    for sprinkler in list_sprinklers: 
        if sprinkler.sprinkler_lock == True:
            write_gpio(sprinkler.sprinkler_gpio, 1)
            lock_gpio(sprinkler.sprinkler_gpio, False)
            logger.info('Sensor GPIO %d is set to HIGH and unlocked', sprinkler.sprinkler_gpio)

def run_scheduler_gpio(sprinkler, setstate, logger):
    gpio = sprinkler.sprinkler_gpio
    if isinstance(gpio, int) == False:
        raise ValueError("run_scheduler_gpio GPIO should be an integer argument!")

#    GPIO.setwarnings(False)
#    GPIO.setmode(GPIO.BCM)
#    GPIO.setup(gpio, GPIO.OUT)
    logger.debug('run_scheduler_gpio GPIO %d it should be %d', gpio, setstate)

    if setstate == 0:
#        sprinkler = Sprinkler.objects.get(sprinkler_gpio__exact=gpio)
        if sprinkler.sprinkler_enabled == True:
        #if gpio not disabled
            if check_if_other_sprinklers_on(gpio) == False:
                #if other gpios not running
                write_gpio(gpio, setstate)
                logger.info('run_scheduler_gpio GPIO %d is set to LOW', gpio)
                return "LOW"
            else:
                logger.debug('run_scheduler_gpio GPIO %d is set to LOW, but other have priority', gpio)
                return "HIGH"
        else:
            logger.debug('run_scheduler_gpio GPIO %d is set to LOW, but is disabled', gpio)
            return "HIGH"
    elif setstate == 1:
        #if not started by hand or sensor
        if sprinkler.sprinkler_lock == False:
            write_gpio(gpio, setstate)
            logger.info('run_scheduler_gpio GPIO %d is set to HIGH', gpio)
            return "HIGH"
        else:
            logger.debug('run_scheduler_gpio GPIO %d is set to HIGH, but is started by others', gpio)
            return "LOW"
    else:
        raise ValueError("run_scheduler_gpio setstate variable should be 0 or 1!")

class SchedulerThread: 
    '''Scheduler thread to run sprinklers in the given time , logger is the log file'''

    def __init__(self): 
        self._running = True
      
    def terminate(self): 
        self._running = False

    def run(self, logger):
        logger.debug('Starting Scheduler loop.')
        while self._running:
            logger.debug('Scheduler check for rain.')
#            rain = check_weather()
            rain = 0
#            logger.info('in loop scheduler')
            if rain == 0:
                logger.debug('Scheduler no rain detected. Check scheduler.')
                list_sprinklers = Sprinkler.objects.order_by('sprinkler_gpio')
                for sprinkler in list_sprinklers: 
                    logger.debug('Check sprinkler %s', sprinkler.sprinkler_name)
                    now_hm = int(datetime.now().strftime('%H'))*60+int(datetime.now().strftime('%M'))
                    sched = Scheduler.objects.get(scheduler_sprinkler_gpio__exact=sprinkler.sprinkler_gpio)
                    logger.debug('%s scheduled between %d and %d, now = %d', sprinkler.sprinkler_name, sched.scheduler_start_time, sched.scheduler_stop_time, now_hm)
                    if sched.scheduler_start_time < sched.scheduler_stop_time:
                        if sched.scheduler_start_time < now_hm < sched.scheduler_stop_time:
                            #start Sprinkler.sprinkler_gpio 
                            run_scheduler_gpio(sprinkler, 0, logger)
                        else:
                            #stop Sprinkler.sprinkler_gpio
                            run_scheduler_gpio(sprinkler, 1, logger)
                    else:
                        if sched.scheduler_start_time < now_hm < 1440 or 0 < now_hm < sched.scheduler_stop_time:
                            #start Sprinkler.sprinkler_gpio 
                            run_scheduler_gpio(sprinkler, 0, logger)
                        else:
                            #stop Sprinkler.sprinkler_gpio
                            run_scheduler_gpio(sprinkler, 1, logger)

            else:
                logger.debug('Scheduler rain detected.')


            logger.debug('End Scheduler loop and wait')
            time.sleep(10)
        
class SensorsThread: 
    '''Sensors thread to run sprinklers when motion detected, logger is the log file'''

    def __init__(self): 
        self._running = True
      
    def terminate(self): 
        self._running = False

    def run(self, logger):
        logger.debug('Starting Sensors loop.')
        while self._running:
            #get status of sensors in code variable (0 = off, 1 = on)
            list_sensors = Sensor.objects.order_by('sensor_gpio')
            code = ''
            for sensor in list_sensors: 
                logger.debug('Check sensor %s', sensor.sensor_name)                
                reading_gpio=read_gpio(sensor.sensor_gpio, 'GPIO.IN')
                logger.debug('Sensor %d is %s', sensor.sensor_gpio, reading_gpio)
                if reading_gpio == 'LOW' and sensor.sensor_enabled:
                    code = ''.join([code, '1'])
                else:
                    code=''.join([code, '0'])
#            code='01'
            logger.debug('Sensor activity code is %s',code)
            #set sprinkler resulted from code 
            sprinkler_to_start = check_code(code)
#            logger.debug('Sesnsor spri is  %d',sprinkler_to_start)
            if sprinkler_to_start != 0:
                stop_all_other_sprinklers(sprinkler_to_start,logger)
                write_gpio(sprinkler_to_start, 0)
                lock_gpio(sprinkler_to_start, True)
                logger.info('Sensor GPIO %d is set to LOW and locked', sprinkler_to_start)
            else:
                stop_all_locked_sprinklers(logger)

            logger.debug('End Sensors loop and wait')
            time.sleep(1)


def run_home(logf):
    '''This does the "work" of the daemon, logf is the log file'''
    #logger will log
    logger = logging.getLogger('autohome_daemon')
#    logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)
    fhandle = logging.FileHandler(logf)
    formatstr = '%(asctime)s (%(levelname)s): %(message)s'
    formatter = logging.Formatter(formatstr)
    fhandle.setFormatter(formatter)
    logger.addHandler(fhandle)

    logger.info('Starting autohome daemon')

    s_schedule = SchedulerThread()
    t_schedule = threading.Thread(target=s_schedule.run, args=(logger,))
    try:
        t_schedule.start()  
    except (KeyboardInterrupt, SystemExit):
        s_schedule.terminate()
        t_schedule.join()

    s_sensors = SensorsThread()
    t_sensors = threading.Thread(target=s_sensors.run, args=(logger,))
    try:
        t_sensors.start()  
    except (KeyboardInterrupt, SystemExit):
        s_sensors.terminate()
        t_sensors.join()

#    while True:
        #threads for mod in [ sense_temp, sense_soil_humidity, sense_light ]:
#        time.sleep(1)

def shutdown(signum, frame):  # signum and frame are mandatory
    sys.exit(0)

def start_daemon(pidf, logf):
    '''This launches the daemon in its context'''
    directory = '/var/lib/autohome_daemon'
    if not os.path.exists(directory):
        os.makedirs(directory)
    ### XXX pidfile is a context
    with daemon.DaemonContext(
        signal_map={
            signal.SIGTERM: shutdown,
            signal.SIGTSTP: shutdown
        },
        working_directory=directory,
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile(pidf),
        ) as context:
        run_home(logf)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autohome daemon!")
    parser.add_argument('-p', '--pid-file', default='/var/run/autohome_daemon.pid')
    parser.add_argument('-l', '--log-file', default='/var/log/autohome_daemon.log')
    args = parser.parse_args()

    start_daemon(pidf=args.pid_file, logf=args.log_file)
