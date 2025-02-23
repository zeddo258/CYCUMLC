from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("student-management/", views.student_management, name="student-management"),
    path("add-student-modal", views.addStudentModal, name="add-student-modal"),
    path("search-students/", views.search_students, name="search_students"),
    path("", views.submit_attendance, name=""),
    path("filter-drop-down/", views.filter_dropdown, name="filter-drop-down"),
    path("filter/", views.filter, name="filter"),
]
