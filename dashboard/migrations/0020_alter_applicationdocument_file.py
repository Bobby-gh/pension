# Generated by Django 3.2.11 on 2022-03-27 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_alter_application_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationdocument',
            name='file',
            field=models.ImageField(null=True, upload_to='uploads/documents'),
        ),
    ]
