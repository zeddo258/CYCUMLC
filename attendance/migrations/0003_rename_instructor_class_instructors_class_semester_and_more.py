# Generated by Django 5.1.3 on 2025-01-13 06:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_class_semester_student_teacher_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='instructor',
            new_name='instructors',
        ),
        migrations.AddField(
            model_name='class',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='attendance.semester'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='attendance.class'),
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='attendance.semester'),
        ),
        migrations.AlterField(
            model_name='attendancerecord',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='attendance.student'),
        ),
        migrations.AlterField(
            model_name='student',
            name='sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10),
        ),
    ]
