# Generated by Django 3.2.11 on 2022-04-22 02:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0009_alter_sysconfig_sms_sender_id'),
        ('dashboard', '0026_rename_inititated_by_sms_initiated_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControllerForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expatriate', models.CharField(blank=True, max_length=100, null=True)),
                ('office', models.CharField(blank=True, max_length=100, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('pensionable_emolument', models.CharField(blank=True, max_length=100, null=True)),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('expatriation_pay', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('other_pensionable_emolument', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('additions_claimed', models.TextField(blank=True, null=True)),
                ('pension_receipt_status', models.CharField(blank=True, max_length=100, null=True)),
                ('commencement_date', models.DateField(blank=True, null=True)),
                ('termination_date', models.DateField(blank=True, null=True)),
                ('leave_withou_pay_from', models.DateField(blank=True, null=True)),
                ('leave_withou_pay_to', models.DateField(blank=True, null=True)),
                ('condonation_authority', models.CharField(blank=True, max_length=100, null=True)),
                ('other_scheduled_work_detail', models.TextField(blank=True, null=True)),
                ('form_5_pensionable_emoluments', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('non_scheduled_work_detail', models.TextField(blank=True, null=True)),
                ('officers_option', models.TextField(blank=True, null=True)),
                ('pension_commencement_date', models.DateField(blank=True, null=True)),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='controller_form', to='dashboard.application')),
                ('retirement_cause', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup.retirementreason')),
            ],
        ),
    ]
