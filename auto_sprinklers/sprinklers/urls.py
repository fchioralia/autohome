"""home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url

from . import views

#app_name = 'sprinklers'
urlpatterns = [
    path('', views.index, name='index'),
    path('sprinkler/<int:sprinkler_gpio>/', views.get_spr_status, name='get_spr_status'),
    path('sensor/<int:sprinkler_gpio>/', views.get_sensor_status, name='get_sensor_status'),
    path('change_sensor_state/<int:sensor_gpio>', views.change_sensor_state, name='change_sensor_state'),
    path('get_sensor_active_state/<int:sensor_gpio>', views.get_sensor_active_state, name='get_sensor_active_state'),
    path('get_scheduler_data/<int:sprinkler_gpio>', views.get_scheduler_data, name='get_scheduler_data'),
    path('set_scheduler_data/<int:sprinkler_gpio>', views.set_scheduler_data, name='set_scheduler_data'),
    path('change_spr_state/<int:sprinkler_gpio>', views.change_spr_state, name='change_spr_state'),
    path('change_spr_active_state/<int:sprinkler_gpio>', views.change_spr_active_state, name='change_spr_active_state'),
    path('set_service_active/<slug:service>/<slug:status>', views.set_service_active, name='set_service_active'),
    path('set_service_enabled/<slug:service>/<slug:status>', views.set_service_enabled, name='set_service_enabled'),
    url('sensor/run/',views.run_sprinklers_service,name='run_sprinklers_service'),
]
