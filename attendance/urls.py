from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('attendance-form/', views.attendance_form, name='attendance-form'),
    path('add-student-modal', views.addStudentModal, name='add-student-modal'),
    path('search-students/', views.search_students, name='search_students'),
    path('select-student/<str:student_id>', views.select_student, name='select-student'),
    path('submit/', views.submit_attendance, name='submit_attendance'),
]

