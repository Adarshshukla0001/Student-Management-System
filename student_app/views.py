from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def student_list(request):
    students = Student.objects.all().order_by('name')
    query = request.GET.get('q')
    if query:
        students = students.filter(name__icontains=query)
    return render(request, 'student_list.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})


def edit_student(request, id):
    student = Student.objects.get(id=id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('student_list')
    return render(request, 'student_form.html', {'form': form})


def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('student_list')
