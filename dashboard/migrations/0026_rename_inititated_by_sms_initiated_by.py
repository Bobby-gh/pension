# Generated by Django 3.2.11 on 2022-04-22 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0025_auto_20220422_0018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sms',
            old_name='inititated_by',
            new_name='initiated_by',
        ),
    ]
