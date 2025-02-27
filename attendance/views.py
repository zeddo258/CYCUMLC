from django.db import models
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from .forms import StudentForm
from .models import Student


def index(request):
    return render(request, "index.html")


def handleAddStudentForm(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            s = form.save()
            context = {"s": s}
            return render(request, "partial/student_information.html", context)

        else:
            print(form.errors)
    return HttpResponseNotFound("Hello world")


def filter(request):
    nations = request.GET.getlist("nation")
    study_times = request.GET.getlist("study_time")
    sex = request.GET.getlist("sex")
    students = Student.objects.all()

    if nations:
        students = students.filter(nationality__in=nations)

    if study_times:
        students = students.filter(study_time__in=study_times)

    if sex:
        students = students.filter(sex__in=sex)
    return render(request, "partial/student_suggestions.html", {"students": students})


def filter_dropdown(request):
    nationality = Student.objects.values_list("nationality", flat=True).distinct()
    study_time = Student.objects.values_list("study_time", flat=True).distinct()
    sex = ["Male", "Female"]
    context = {
        "nationality": nationality,
        "study_time": study_time,
        "sex": sex,
    }
    return render(request, "partial/filter-drop-down.html", context)


def student_management(request):
    """
    if request.user.is_authenticated:
        redirect('login')
    """
    # Render the student list
    students = Student.objects.all()

    # Render the filter box
    nationality = Student.objects.values_list("nationality", flat=True).distinct()
    study_time = Student.objects.values_list("study_time", flat=True).distinct()
    sex = ["Male", "Female"]

    context = {
        "students": students,
        "nationality": nationality,
        "study_time": study_time,
        "sex": sex,
        "form": StudentForm(),
    }
    return render(request, "partial/crud_students.html", context)


def search_students(request):

    query = request.GET.get("studentSearch", "").strip()  # 使用者打的文字
    print("Debug | search_students - query:", query)  # 印出 query 值
    students = []
    if query:
        # 範例：以姓名或學號做簡單篩選
        students = Student.objects.filter(
            models.Q(chinese_name__icontains=query)
            | models.Q(id__icontains=query)
            | models.Q(nationality__icontains=query)
            | models.Q(study_time__icontains=query)
        )
    else:
        students = Student.objects.all()
    return render(request, "partial/student_suggestions.html", {"students": students})
