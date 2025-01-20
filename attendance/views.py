from django.shortcuts import render, redirect
from .forms import AttendanceForm
from .models import AttendanceRecord
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

def test1(request):
    return render(request, 'partial/test1.html')


def test2(request):
    return render(request, 'partial/test2.html')

def test3(request):
    return render(request, 'partial/test3.html')

def index(request):
    '''
    if request.user.is_authenticated:
        redirect('login')
    '''
    return render(request, 'index.html')

def login_user(request):
    """
    Handle user login with HTMX.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Return a success message or redirect to a dashboard
            return redirect('index')         
    return render(request, 'login.html')

def record_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_success')  # Redirect to a success page or another view
    else:
        form = AttendanceForm()

    return render(request, 'attendance/record_attendance.html', {'form': form})

