# Generated by Django 2.2.12 on 2020-04-02 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduler_sprinkler_gpio', models.IntegerField(default=0)),
                ('scheduler_start_time', models.TimeField()),
                ('scheduler_stop_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_gpio', models.IntegerField(default=0)),
                ('sensor_state', models.BooleanField(default=False)),
                ('sensor_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sprinkler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sprinkler_gpio', models.IntegerField(default=0)),
                ('sprinkler_state', models.BooleanField(default=False)),
                ('sprinkler_name', models.CharField(max_length=50)),
            ],
        ),
    ]
