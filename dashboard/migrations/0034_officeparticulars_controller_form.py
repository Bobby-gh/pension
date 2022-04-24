# Generated by Django 3.2.11 on 2022-04-23 23:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0033_officeparticulars'),
    ]

    operations = [
        migrations.AddField(
            model_name='officeparticulars',
            name='controller_form',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='office_particulars', to='dashboard.controllerform', verbose_name='Controller Form'),
            preserve_default=False,
        ),
    ]
