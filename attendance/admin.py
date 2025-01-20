from django.contrib import admin
from attendance.models import AttendanceRecord, Student, Class, Semester, Teacher

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status', 'hours_attended')
    # exclude = ('status', 'hours_attended')
    search_fields = ('student__chinese_name', 'student__english_name', 'course__name', 'semester__semester_name')
    list_filter = ('status', )
    autocomplete_fields = ['student', 'course']  # Enable autocomplete
    def save_model(self, request, obj, form, change):
        # Calculate attendance before saving
        obj.calculate_hours_attended()
        super().save_model(request, obj, form, change)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ('chinese_name', 'english_name')  # Fields used for search in admin

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    search_fields = ('chinese_name',)  # Fields for teacher search
