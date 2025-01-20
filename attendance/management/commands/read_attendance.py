from django.core.management.base import BaseCommand
from attendance.models import AttendanceRecord, Student

class Command(BaseCommand):
    help = 'Read attendance records for a specific student using their ID'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=str, help='Student ID to fetch attendance records for')

    def handle(self, *args, **options):
        student_id = options['student_id']
        try:
            student = Student.objects.get(id=student_id)
            attendance_records = AttendanceRecord.objects.filter(student=student)

            if not attendance_records.exists():
                self.stdout.write(f"No attendance records found for student: {student.english_name} (ID: {student_id})")
                return

            self.stdout.write(f"Attendance Records for {student.english_name} (ID: {student_id}):")
            for record in attendance_records:
                self.stdout.write(f"- Date: {record.date}, Course: {record.course.name}, "
                                  f"Status: {record.status}, Hours Attended: {record.hours_attended}")
        except Student.DoesNotExist:
            self.stderr.write(f"Student with ID '{student_id}' does not exist.")

