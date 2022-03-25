# Generated by Django 3.2.11 on 2022-03-24 16:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0001_initial'),
        ('dashboard', '0017_notification_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationdocument',
            name='document_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documents', to='setup.applicationdocumenttype'),
        ),
        migrations.AlterField(
            model_name='applicationrank',
            name='rank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.rank'),
        ),
        migrations.DeleteModel(
            name='ApplicationDocumentType',
        ),
        migrations.DeleteModel(
            name='Rank',
        ),
    ]
