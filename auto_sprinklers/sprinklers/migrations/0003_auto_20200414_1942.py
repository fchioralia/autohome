# Generated by Django 2.2.12 on 2020-04-14 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprinklers', '0002_sprinkler_sprinkler_active_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduler',
            name='scheduler_start_time',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='scheduler',
            name='scheduler_stop_time',
            field=models.IntegerField(),
        ),
    ]
