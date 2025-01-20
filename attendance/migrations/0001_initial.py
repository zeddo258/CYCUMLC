# Generated by Django 5.1.3 on 2025-01-13 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
                ('course_id', models.IntegerField()),
                ('semester_id', models.IntegerField()),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')], default='Present', max_length=10)),
                ('hours_attended', models.DecimalField(decimal_places=2, default=1.0, max_digits=5)),
                ('remark', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
