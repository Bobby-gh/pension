# Generated by Django 3.2.11 on 2022-03-25 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_auto_20220324_1640'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'permissions': (('can_review_application', 'Change application status'), ('can_generate_letter', 'Generate award letter from application'))},
        ),
    ]
