from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Sprinkler, Sensor, Scheduler

admin.site.register(Sensor)
admin.site.register(Sprinkler)
admin.site.register(Scheduler)
