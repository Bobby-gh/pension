# Generated by Django 3.2.11 on 2022-04-21 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0003_auto_20220325_0130'),
    ]

    operations = [
        migrations.AddField(
            model_name='rank',
            name='abbreviation',
            field=models.CharField(default='', max_length=20),
        ),
    ]
