from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("student-management/", views.student_management, name="student-management"),
    path(
        "student-form-handler/", views.handleAddStudentForm, name="student-form-handler"
    ),
    path("search-students/", views.search_students, name="search_students"),
    path("filter-drop-down/", views.filter_dropdown, name="filter-drop-down"),
    path("filter/", views.filter, name="filter"),
]
