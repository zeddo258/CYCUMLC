# Generated by Django 5.1.6 on 2025-03-01 02:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0009_alter_attendancerecord_arrival_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='first_date',
            field=models.DateField(default=datetime.datetime(2025, 3, 1, 2, 24, 34, 271610)),
        ),
    ]
