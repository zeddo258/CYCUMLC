from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import AttendanceForm
from .models import AttendanceRecord, Class, Student


def index(request):
    return render(request, 'index.html')

def attendance_form(request):
    '''
    if request.user.is_authenticated:
        redirect('login')
    '''

    students = Student.objects.all()
    return render(request, 'partial/crud_students.html', {
        'students': students
    })


def search_students(request):
    """根據前端輸入的文字，動態回傳符合的學生清單"""

    query = request.GET.get('studentSearch', '').strip()  # 使用者打的文字
    print("Debug | search_students - query:", query)  # 印出 query 值
    students = []
    if query:
        # 範例：以姓名或學號做簡單篩選
        students = Student.objects.filter(
            models.Q(id__icontains=query)
        )    
    else:
        students = Student.objects.all()
    return render(request, 'partial/student_suggestions.html', {
        'students': students
    })

# Reponse with html that displace the student information
def select_student(request, student_id):
    print("Debug | select_student - student_id:", student_id)
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'partial/student_selected.html', {
        'student':student
    })


def submit_attendance(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        class_id = request.POST.get('class_id')
        date = request.POST.get('date')
        arrival_time = request.POST.get('arrival_time')
        
        # 例外處理略
        student = Student.objects.get(id=student_id)
        student_class = Class.objects.get(id=class_id)

        AttendanceRecord.objects.create(
            student=student,
            student_class=student_class,
            date=date,
            arrival_time=arrival_time
        )

        return render(request, 'attendance_form.html', {
            'classes': Class.objects.all(),
            'success': True
        })

    return render(request, 'attendance_form.html', {
        'classes': Class.objects.all()
    })

