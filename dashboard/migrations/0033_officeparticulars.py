# Generated by Django 3.2.11 on 2022-04-23 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0032_servicebreak'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeParticulars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('if_pensionable', models.CharField(max_length=200)),
                ('commencement_date', models.DateField(blank=True, null=True)),
                ('termination_date', models.DateField(blank=True, null=True)),
                ('emoluments', models.TextField()),
            ],
        ),
    ]
