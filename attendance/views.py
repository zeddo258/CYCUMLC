from django.db import models
from django.shortcuts import get_object_or_404, render
from .forms import StudentForm
from .models import AttendanceRecord, Class, Student




def index(request):
    return render(request, "index.html")

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
    sex = ["Male","Female"]
    context = {
        "nationality" : nationality,
        "study_time" : study_time,
        "sex" : sex,
    }
    return render(request, "partial/filter-drop-down.html", context)


def addStudentModal(request):
    return render(request, "partial/add_student_modal.html")


def student_management(request):
    """
    if request.user.is_authenticated:
        redirect('login')
    """

    students = Student.objects.all()
    nationality = Student.objects.values_list("nationality", flat=True).distinct()
    study_time = Student.objects.values_list("study_time", flat=True).distinct()
    sex = ["Male","Female"]
    context = {
        "students" : students,
        "nationality" : nationality,
        "study_time" : study_time,
        "sex" : sex,
        "form" : StudentForm(),
    }
    return render(request, "partial/crud_students.html", context)


def search_students(request):
    """根據前端輸入的文字，動態回傳符合的學生清單"""

    query = request.GET.get("studentSearch", "").strip()  # 使用者打的文字
    print("Debug | search_students - query:", query)  # 印出 query 值
    students = []
    if query:
        # 範例：以姓名或學號做簡單篩選
        students = Student.objects.filter( 
                                          models.Q(chinese_name__icontains=query) |
                                          models.Q(id__icontains=query) |
                                          models.Q(nationality__icontains=query) |
                                          models.Q(study_time__icontains=query)
                                          )
    else:
        students = Student.objects.all()
    return render(request, "partial/student_suggestions.html", {"students": students})


# Reponse with html that displace the student information
def select_student(request, student_id):
    print("Debug | select_student - student_id:", student_id)
    student = get_object_or_404(Student, pk=student_id)
    return render(request, "partial/student_selected.html", {"student": student})


def submit_attendance(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        class_id = request.POST.get("class_id")
        date = request.POST.get("date")
        arrival_time = request.POST.get("arrival_time")

        # 例外處理略
        student = Student.objects.get(id=student_id)
        student_class = Class.objects.get(id=class_id)

        AttendanceRecord.objects.create(
            student=student,
            student_class=student_class,
            date=date,
            arrival_time=arrival_time,
        )

        return render(
            request,
            "attendance_form.html",
            {"classes": Class.objects.all(), "success": True},
        )

    return render(request, "attendance_form.html", {"classes": Class.objects.all()})
