# Generated by Django 3.2.11 on 2022-04-22 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_totalpensionableemolumentdrawnbeforeretirement'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TotalPensionableEmolumentDrawnBeforeRetirement',
            new_name='PensionableEmolumentDrawnBeforeRetirement',
        ),
    ]
