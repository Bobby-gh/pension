# Generated by Django 3.2.11 on 2022-03-27 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0003_auto_20220325_0130'),
        ('dashboard', '0020_alter_applicationdocument_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationdocument',
            name='document_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='setup.applicationdocumenttype'),
        ),
    ]
