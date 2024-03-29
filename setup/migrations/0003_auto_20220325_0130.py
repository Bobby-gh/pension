# Generated by Django 3.2.11 on 2022-03-25 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0002_setupperms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='setupperms',
            options={'default_permissions': (), 'managed': False, 'permissions': (('can_setup_system', 'Can Setup System'), ('can_managemnt_roles', 'Can Management role assignment user groups.'))},
        ),
        migrations.AlterField(
            model_name='rank',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
