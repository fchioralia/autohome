#!/usr/bin/python3
'''daemon for controling home 
gets data from sensors/schedule/etc.. and control the GPIOs'''
import time
import argparse
import logging
import os
import sys
import daemon
from daemon import pidfile
import signal
import threading
import django

script_path = os.path.dirname(__file__)
os.environ['DJANGO_SETTINGS_MODULE']='home.settings'
django.setup()

#from django.models import Sp
from sprinklers.models import Sprinkler, Sensor, Scheduler

class Scheduler: 

    def __init__(self): 
        self._running = True
      
    def terminate(self): 
        self._running = False

    def run(self, logger):
        logger.debug('Starting Scheduler loop ')
        while self._running:
            logger.info('in loop scheduler')
            list_sprinklers = Sprinkler.objects.order_by('sprinkler_gpio')
            for sprinkler in list_sprinklers: 
                logger.debug('Sprinkler %s', sprinkler.sprinkler_gpio)

            logger.debug('End Scheduler loop and wait')
            time.sleep(10)
        


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

#    schedule = getattr(autohome_mods, 'scheduler')
    # worker now is a reference to the function like alice.do_work
    s_schedule=Scheduler()
    t_schedule = threading.Thread(target=s_schedule.run, args=(logger,))
    try:
        t_schedule.start()  
    except (KeyboardInterrupt, SystemExit):
        s_schedule.terminate()
        t_schedule.join()

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
