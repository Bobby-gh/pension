# Generated by Django 3.2.11 on 2022-03-24 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SetupPerms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('can_setup_system', 'Can Setup System'),),
                'managed': False,
                'default_permissions': (),
            },
        ),
    ]
