# Generated by Django 3.2.11 on 2022-04-21 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0006_alter_retirementreason_description'),
        ('dashboard', '0021_alter_applicationdocument_document_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='reason',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup.retirementreason'),
        ),
    ]
