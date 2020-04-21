from django.shortcuts import render
from django.http import Http404
#from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
#from django.template import loader
#from background_task import background
import sys
import os
import RPi.GPIO as GPIO

from .models import Sprinkler, Sensor, Scheduler

def index(request):
    list_sprinklers = Sprinkler.objects.order_by('sprinkler_gpio')
    list_sensors = Sensor.objects.order_by('sensor_gpio')
    service_active_autohome = get_service_active("autohome")
    service_enabled_autohome = get_service_enabled("autohome")
#    template = loader.get_template('sprinklers/index.html')
    context = {
        'list_sprinklers': list_sprinklers,
        'list_sensors': list_sensors,
        'service_active_autohome': service_active_autohome,
        'service_enabled_autohome': service_enabled_autohome,
    }
    return render(request, 'sprinklers/index.html', context )
#    output = ', '.join([q.sprinkler_name for q in list_sprinklers])
#    return HttpResponse(output)


def get_service_active(service):
    command="/bin/systemctl is-active --quiet "+service
    status=os.system(command)
    if status == 0:
        return True
    else:
        return False

def set_service_active(request, service, status):
    command="/bin/systemctl is-active --quiet "+service
    realstatus=os.system(command)
    if status == "on" and realstatus != 0:
        os.system("/bin/systemctl start "+service)
    elif status == "off" and realstatus == 0:
        os.system("/bin/systemctl stop "+service)

    return JsonResponse({"service": service, "status": status}, status=200)

def get_service_enabled(service):
    command="/bin/systemctl is-enabled --quiet "+service
    status=os.system(command)
    if status == 0:
        return True
    else:
        return False

def set_service_enabled(request, service, status):
    command="/bin/systemctl is-enabled --quiet "+service
    realstatus=os.system(command)
    if status == "on" and realstatus != 0:
        os.system("/bin/systemctl enable "+service)
    elif status == "off" and realstatus == 0:
        os.system("/bin/systemctl disable "+service)

    return JsonResponse({"service": service, "status": status}, status=200)

def get_scheduler_data(request, sprinkler_gpio):
    try:
        scheduler = Scheduler.objects.get(scheduler_sprinkler_gpio__exact=sprinkler_gpio)
    except Scheduler.DoesNotExist:
        raise Http404("No sprinkler found with gpio= %d!" % (scheduler_sprinkler_gpio))
    return JsonResponse({"scheduler_sprinkler_gpio": scheduler.scheduler_sprinkler_gpio,
        "scheduler_start_time": scheduler.scheduler_start_time,
        "scheduler_stop_time": scheduler.scheduler_stop_time}, status=200)

def set_scheduler_data(request, sprinkler_gpio):
    try:
        scheduler = Scheduler.objects.get(scheduler_sprinkler_gpio__exact=sprinkler_gpio)
    except Scheduler.DoesNotExist:
        Scheduler.objects.create(
            scheduler_sprinkler_gpio = sprinkler_gpio,
            scheduler_start_time = request.POST['scheduler_start_time'],
            scheduler_stop_time = request.POST['scheduler_stop_time']
        )
#        scheduler.save()
#        raise Http404("No sprinkler found with gpio= %d!" % (sprinkler_gpio))
    else:
        scheduler.scheduler_start_time = request.POST['scheduler_start_time']
        scheduler.scheduler_stop_time = request.POST['scheduler_stop_time']
        scheduler.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return JsonResponse({"sprinkler_gpio": sprinkler_gpio}, status=200)


def get_sprinkler_enabled(request, sprinkler_gpio):
    try:
        sprinkler = Sprinkler.objects.get(sprinkler_gpio__exact=sprinkler_gpio)
    except Sprinkler.DoesNotExist:
        raise Http404("No sprinkler found with gpio= %d!" % (sprinkler_gpio))
    return render(request, 'sprinklers/sprinkler.html', {'sprinkler': sprinkler})

def get_sensor_enabled(request, sensor_gpio):
    try:
        sprinkler = Sensor.objects.get(sensor_gpio__exact=sensor_gpio)
    except Sensor.DoesNotExist:
        raise Http404("No sensor found with gpio= %d!" % (sensor_gpio))
    return render(request, 'sprinklers/sensor.html', {'sensor': sensor})

def get_sensor_active_state(request, sensor_gpio):
    try:
        sprinkler = Sensor.objects.get(sensor_gpio__exact=sensor_gpio)
    except Sensor.DoesNotExist:
        raise Http404("No sensor found with gpio= %d!" % (sensor_gpio))
    else:
        reading_gpio=read_gpio(sensor_gpio, 'GPIO.IN')
        return JsonResponse({"sensor_active_state": reading_gpio}, status=200)

def set_sprinkler_enabled(request, sprinkler_gpio):
    try:
        sprinkler = Sprinkler.objects.get(sprinkler_gpio__exact=sprinkler_gpio)
    except Sprinkler.DoesNotExist:
        raise Http404("No sprinkler found with gpio= %d!" % (sprinkler_gpio))
    else:
        if sprinkler.sprinkler_enabled :
            write_gpio(sprinkler.sprinkler_gpio, 1)
            sprinkler.sprinkler_enabled = False
            sprinkler.sprinkler_lock = False
            sprinkler.save()
        else:
            sprinkler.sprinkler_enabled = True
            sprinkler.save()
    return JsonResponse({"sprinkler_gpio": sprinkler_gpio}, status=200)

def set_sensor_enabled(request, sensor_gpio):
    try:
        sensor = Sensor.objects.get(sensor_gpio__exact=sensor_gpio)
    except Sensor.DoesNotExist:
        raise Http404("No sensor found with gpio= %d!" % (sensor_gpio))
    else:
        if sensor.sensor_state :
            sensor.sensor_state = False
            sensor.save()
        else:
            sensor.sensor_state = True
            sensor.save()
    return JsonResponse({"sensor_gpio": sensor_gpio}, status=200)

''' change a state of a sprinkler '''
def set_sprinkler_active(request, sprinkler_gpio):
    try:
        sprinkler = Sprinkler.objects.get(sprinkler_gpio__exact=sprinkler_gpio)
    except Sprinkler.DoesNotExist:
        raise Http404("No sprinkler found with gpio= %d!" % (sprinkler_gpio))
    else:
        reading_gpio=read_gpio(sprinkler_gpio, 'GPIO.OUT')
        if  reading_gpio == "LOW":
            write_gpio(sprinkler_gpio, 1)
            sprinkler.sprinkler_lock = False
            sprinkler.save()
        else:
            if  sprinkler.sprinkler_enabled == True :
                write_gpio(sprinkler_gpio, 0)
                sprinkler.sprinkler_lock = True
                sprinkler.save()
    return JsonResponse({"sprinkler_gpio": sprinkler_gpio}, status=200)

'''Manage input of the sensor given by first argument = gpio bcm port and mode in/out'''
'''read the gpio at "port" number and inout is GPIO.IN or GPIO.OUT'''
def read_gpio(port, inout):
    if isinstance(port, int) == False:
        raise ValueError("port should be an integer argument!")
    if inout == "GPIO.OUT":
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(port, GPIO.OUT)

        i = GPIO.input(port)
        if i == 0:
            return "LOW"
        else:
            return "HIGH"

    elif inout == "GPIO.IN":
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(port, GPIO.IN)

        i = GPIO.input(port)
        if i == 0:
            return "HIGH"
        else:
            return "LOW"

    else:
        raise ValueError("inout should be GPIO.IN or GPIO.OUT!")

'''Manage output of the sensor given by first argument = gpio bcm out port and setstate (0 or 1)'''
def write_gpio(outport, setstate):
    if isinstance(outport, int) == False:
        raise ValueError("port should be an integer argument!")

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(outport, GPIO.OUT)
    if setstate == 0:
        GPIO.output(outport, GPIO.LOW)
        return "LOW"
    elif setstate == 1:
        GPIO.output(outport, GPIO.HIGH)
        return "HIGH"
    else:
        raise ValueError("setstate should be 0 or 1!")


