# Generated by Django 3.2.11 on 2022-04-24 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0035_alter_officeparticulars_if_pensionable'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='open_vote_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]