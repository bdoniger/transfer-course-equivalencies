# Generated by Django 4.1.5 on 2023-04-30 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TransferGuide', '0019_autoreplyemail_for_admins_autoreplyemail_reply_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autoreplyemail',
            name='for_admins',
        ),
        migrations.RemoveField(
            model_name='autoreplyemail',
            name='reply',
        ),
    ]