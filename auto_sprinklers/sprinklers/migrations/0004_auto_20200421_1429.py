# Generated by Django 2.2.12 on 2020-04-21 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprinklers', '0003_auto_20200414_1942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sprinkler',
            old_name='sprinkler_active_state',
            new_name='sprinkler_enabled',
        ),
        migrations.RenameField(
            model_name='sprinkler',
            old_name='sprinkler_state',
            new_name='sprinkler_lock',
        ),
    ]
