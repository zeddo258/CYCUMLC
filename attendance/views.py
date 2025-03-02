from datetime import datetime

from django.db import models
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from .forms import StudentForm
from .models import Student


def index(request):
    return render(request, "index.html")


def editStudentInfo(request, student_id):
    student = Student.objects.get(id=student_id)

    html_date_format = student.birth.strftime("%Y-%m-%d")
    html_first_date = student.first_date.strftime("%Y-%m-%d")
    print(html_first_date)
    context = {
        "s": student,
        "formatted_date": html_date_format,
        "formatted_first_day": html_first_date,
    }
    return render(request, "components/edit_student_modal.html", context)


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
    sex = request.GET.getlist("sex")
    students = Student.objects.all()

    if nations:
        students = students.filter(nationality__in=nations)

    if sex:
        students = students.filter(sex__in=sex)
    return render(request, "partial/student_suggestions.html", {"students": students})


def get_nation(request):
    nationality = Student.objects.values_list("nationality", flat=True).distinct()
    # store the state of checked nation
    selected_nations = request.GET.getlist("nation")

    marked_nationality = [
        {"nation": nation, "selected": nation in selected_nations}
        for nation in nationality
    ]

    context = {
        "nationality": marked_nationality,
    }
    return render(request, "components/nation-list.html", context)


def student_management(request):
    """
    if request.user.is_authenticated:
        redirect('login')
    """
    # Render the student list
    students = Student.objects.all()

    # Render the filter box
    nationality = Student.objects.values_list("nationality", flat=True).distinct()

    marked_nationality = [
        {"nation": nation, "selected": None} for nation in nationality
    ]

    sex = ["Male", "Female"]

    context = {
        "students": students,
        "nationality": marked_nationality,
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
        )
    else:
        students = Student.objects.all()
    return render(request, "partial/student_suggestions.html", {"students": students})
