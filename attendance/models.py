from datetime import datetime, time, timedelta

from django.db import models


class Semester(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    semester_name = models.CharField(
        max_length=50, unique=True
    )  # Example: '2024 Spring'
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.semester_name


class Teacher(models.Model):
    id = models.CharField(
        unique=True, max_length=255, primary_key=True
    )  # Unique ID for each teacher
    chinese_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.chinese_name} (ID: {self.id})"


class Class(models.Model):
    # Format: year/month/day/className
    # Date specifies the semester starting date
    id = models.CharField(unique=True, max_length=255, primary_key=True)
    name = models.CharField(max_length=2)
    instructors = models.ManyToManyField(
        Teacher, related_name="classes"
    )  # Many-to-many relationship with teachers
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, related_name="classes"
    )  # Link to Semester

    def __str__(self):
        return f"{self.name} ({self.semester.semester_name})"


class Student(models.Model):
    id = models.CharField(
        max_length=255, unique=True, primary_key=True
    )  # Unique ID for each student
    chinese_name = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255)
    sex = models.CharField(
        max_length=10, choices=[("Male", "Male"), ("Female", "Female")]
    )
    birth = models.DateField()
    nationality = models.CharField(max_length=255)
    first_date = models.DateField(default=datetime.now())

    def __str__(self):
        return f"{self.chinese_name} (ID: {self.id})"
