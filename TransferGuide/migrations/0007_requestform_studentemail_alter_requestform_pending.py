# Generated by Django 4.1.5 on 2023-03-31 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TransferGuide', '0006_requestform_approve_requestform_pending_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestform',
            name='studentEmail',
            field=models.CharField(default='N/A', max_length=1000),
        ),
        migrations.AlterField(
            model_name='requestform',
            name='pending',
            field=models.BooleanField(default=True),
        ),
    ]
