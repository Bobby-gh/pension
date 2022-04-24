# Generated by Django 3.2.11 on 2022-04-22 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_controllerform'),
    ]

    operations = [
        migrations.AddField(
            model_name='controllerform',
            name='total_emolument',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='controllerform',
            name='condonation_authority',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='controllerform',
            name='expatriate',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='controllerform',
            name='office',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='controllerform',
            name='pension_receipt_status',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='controllerform',
            name='pensionable_emolument',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]