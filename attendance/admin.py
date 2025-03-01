from django.contrib import admin

from attendance.models import Class, Semester, Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ("chinese_name", "english_name")  # Fields used for search in admin


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    search_fields = ("chinese_name",)  # Fields for teacher search
