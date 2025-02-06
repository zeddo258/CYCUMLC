from django.urls import path

from . import views

urlpatterns = [
    path('', views.attendance_form, name='attendance_form'),
    path('search-students/', views.search_students, name='search_students'),
    path('select-student/<str:student_id>', views.select_student, name='select-student'),
    path('submit/', views.submit_attendance, name='submit_attendance'),
]

