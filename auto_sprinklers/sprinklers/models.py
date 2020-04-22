from django.db import models

# Create your models here.

class Sensor(models.Model):
    sensor_gpio = models.IntegerField(default=0)
    sensor_enabled = models.BooleanField(default=False)
    sensor_name = models.CharField(max_length=50)

    def __str__(self):
        return self.sensor_name


class Sprinkler(models.Model):
    sprinkler_gpio = models.IntegerField(default=0)
    sprinkler_lock =  models.BooleanField(default=False)
    sprinkler_enabled =  models.BooleanField(default=False)
    sprinkler_name = models.CharField(max_length=50)

    def __str__(self):
        return self.sprinkler_name

class Scheduler(models.Model):

    scheduler_sprinkler_gpio = models.IntegerField(default=0)
    scheduler_start_time = models.IntegerField()
    scheduler_stop_time = models.IntegerField()

class Code(models.Model):

    code_sprinkler_gpio = models.IntegerField(default=0)
    code_value = models.CharField(max_length=50)
