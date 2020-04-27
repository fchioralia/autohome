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
import requests
import json

script_path = os.path.dirname(__file__)
os.environ['DJANGO_SETTINGS_MODULE']='home.settings'
django.setup()

from sprinklers.models import Sprinkler, Sensor, Scheduler, Code, Priority
from sprinklers.views import read_gpio, write_gpio, lock_gpio, check_code, stop_all_locked_sprinklers, stop_others_with_lower_priority

def check_weather():
    ''' connect to openweather and return 1 if there is rain in the next 24h or min_temp > 277Kelvin'''
    on = 0
    outjson = "forecast.json"
    apikey = "117f04a82298fb8e296bb5ee7eb543d6"
    bragadiru = 683914
    url = "https://api.openweathermap.org/data/2.5/forecast?id="+str(bragadiru)+"&APPID="+str(apikey)

    if not os.path.isfile(outjson):
        os.mknod(outjson)

    fileTIMEnow=time.time()
    fileTIMEmodified=os.path.getmtime(outjson)

    if ( fileTIMEnow-fileTIMEmodified > 62400 ) or os.stat(outjson).st_size == 0:
        #download only if older then 24h or greater than 0
        r = requests.get(url)
        jsonu = r.json()
        with open(outjson, 'wb') as f:
            f.write(r.content)
    else:
        with open(outjson) as json_file:
            jsonu = json.load(json_file)

    for list in jsonu['list']:
        if list['main']['temp_min'] < 277.15 :
            on = 1
        for weather in list['weather']:
            if weather['main'] == "Rain" :
                on = 1
    return on

def set_gpio(sprinkler, setstate, priority_name, logger):
    gpio = sprinkler.sprinkler_gpio
    if isinstance(gpio, int) == False:
        raise ValueError("set_gpio GPIO should be an integer argument!")

    try:
        prio = Priority.objects.get(priority_name__exact=priority_name)
    except Priority.DoesNotExist:
        priority_value=0
    else:
        priority_value=prio.priority_value

    logger.debug('start set_gpio %d to %d with priority %d', gpio, setstate, priority_value)

    if setstate == 0:
        #if gpio not disabled
        if sprinkler.sprinkler_enabled == True:
            #stop_others_with_lower_priority('priority_name')
            all_off = stop_others_with_lower_priority(priority_name)
            if all_off == 0:
                #if other gpios not running
                write_gpio(gpio, setstate)
                lock_gpio(gpio, priority_value)
                logger.info('set_gpio GPIO %d to LOW', gpio)
                return "LOW"
            else:
                logger.debug('set_gpio GPIO %d to LOW not performed, low priority', gpio)
                return "HIGH"
        else:
            logger.debug('set_gpio GPIO %d to LOW not performed, disabled', gpio)
            return "HIGH"
    elif setstate == 1:
        #if not started by higher prio
        logger.info('set_gpio %d prio is %d ',gpio, priority_value)
        if sprinkler.sprinkler_lock <= priority_value:
            lock_gpio(gpio, 0)
            write_gpio(gpio, setstate)
            logger.info('set_gpio GPIO %d to HIGH', gpio)
            return "HIGH"
        else:
            logger.debug('set_gpio GPIO %d to HIGH, not performed, low priority', gpio)
            return "LOW"
    else:
        raise ValueError("set_gpio setstate variable should be 0 or 1!")

class SchedulerThread: 
    '''Scheduler thread to run sprinklers in the given time , logger is the log file'''

    def __init__(self): 
        self._running = True
      
    def terminate(self): 
        self._running = False

    def run(self, logger):
        logger.debug('Starting Scheduler loop.')
        while self._running:
            rain = check_weather()
            logger.debug('Scheduler check for rain. result= %d', rain)
#            rain = 0
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
                            set_gpio(sprinkler, 0, 'scheduler', logger)
                        else:
                            #stop Sprinkler.sprinkler_gpio
                            set_gpio(sprinkler, 1, 'scheduler', logger)
                    else:
                        if sched.scheduler_start_time < now_hm < 1440 or 0 < now_hm < sched.scheduler_stop_time:
                            #start Sprinkler.sprinkler_gpio 
                            set_gpio(sprinkler, 0, 'scheduler', logger)
                        else:
                            #stop Sprinkler.sprinkler_gpio
                            set_gpio(sprinkler, 1, 'scheduler', logger)

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
            #stop_other_if_priority_lower
                check_gpio=read_gpio(sprinkler_to_start,'GPIO.OUT')
                if check_gpio == 'HIGH':
                    stop_all_locked_sprinklers('sensor')
                sprinkler = Sprinkler.objects.get(sprinkler_gpio__exact=sprinkler_to_start)
                set_gpio(sprinkler, 0, 'sensor', logger)
            else:
            #stop_all_locked_by_sensor
                stop_all_locked_sprinklers('sensor')
                logger.debug('Sensors stop all with the same priority')

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
    if (logger.hasHandlers()):
        logger.handlers.clear()
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
