from datetime import datetime, time, timedelta

from django.db import models


class Semester(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    semester_name = models.CharField(max_length=50, unique=True)  # Example: '2024 Spring'
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.semester_name


class Teacher(models.Model):
    id = models.CharField(unique=True, max_length=255, primary_key=True)  # Unique ID for each teacher
    chinese_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.chinese_name} (ID: {self.id})"


class Class(models.Model):
    # Format: year/month/day/className
    # Date specifies the semester starting date
    id = models.CharField(unique=True, max_length=255, primary_key=True)
    name = models.CharField(max_length=2)
    instructors = models.ManyToManyField(Teacher, related_name='classes')  # Many-to-many relationship with teachers
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='classes')  # Link to Semester

    def __str__(self):
        return f"{self.name} ({self.semester.semester_name})"


class Student(models.Model):
    id = models.CharField(max_length=255,unique=True, primary_key=True)  # Unique ID for each student
    chinese_name = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    birth = models.DateField()
    nationality = models.CharField(max_length=255)
    study_time = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.chinese_name} (ID: {self.id})"

    def get_class_start_times(self):
        """
        Extract class start times from the study_time field.
        """
        study_time = self.study_time  # Example: "3hr(9-12)"
        if '(' in study_time:
            time_range = study_time.split('(')[1].strip(')')
            start_hour, end_hour = map(int, time_range.split('-'))
            return [time(hour, 10) for hour in range(start_hour, end_hour)]
        return []


class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    arrival_time = models.TimeField(default=time(17,0))
    status = models.CharField(
        max_length=10,
        choices=[
            ('Present', 'Present'),
            ('Absent', 'Absent'),
            ('Late', 'Late')
        ],
        default='Present'
    )
    hours_attended = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Attendance: {self.student.english_name} for {self.course.name} on {self.date}"


    def calculate_hours_attended(self):
        """
        Calculate hours attended based on the student's arrival time and the relevant class start time.
        """
        # Get the class start times from the student's study_time
        class_start_times = self.student.get_class_start_times()
        # Find the relevant start time for this arrival time
        relevant_start_time = None
        arrival_time = datetime.combine(datetime.min, self.arrival_time)
        for start_time in class_start_times:
            start_time_min = datetime.combine(datetime.min, start_time)
            time_diff = arrival_time - start_time_min
            print(f"------------------Time diff: {time_diff}")
            if ( time_diff < timedelta(hours=1) ):
                relevant_start_time = start_time
                break
                print(f"--------------------Time:{relevant_start_time}")

        if not relevant_start_time:
            # No valid start time available
            self.status = 'Absent'
            self.hours_attended = 0
            return

        # Convert times to timedelta for calculation
        start_delta = timedelta(hours=relevant_start_time.hour, minutes=relevant_start_time.minute)
        arrival_delta = timedelta(hours=self.arrival_time.hour, minutes=self.arrival_time.minute)

        # Determine status and hours attended
        if arrival_delta <= start_delta + timedelta(minutes=5):  # On time (within 5 minutes)
            self.status = 'Present'
            self.hours_attended = 1.0
        else:  # Late
            time_diff = (arrival_delta - start_delta).total_seconds() / 60
            self.status = 'Late'
            self.hours_attended = 1.0 - round(time_diff / 50, 2)
