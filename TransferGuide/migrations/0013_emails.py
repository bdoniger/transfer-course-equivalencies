# Generated by Django 4.1.5 on 2023-04-13 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TransferGuide', '0012_acronym_rename_university_course_universityshort_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='N/A', max_length=200)),
                ('content', models.CharField(default='N/A', max_length=5000)),
                ('studentEmail', models.CharField(default='N/A', max_length=1000)),
                ('status', models.CharField(default='Unread', max_length=7)),
                ('studentName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
