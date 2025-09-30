from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import logging
# Create your views here.
def index(request):
    return render(request, "ToDo/index.html")

def show_tasks(request):
    user = request.user
    tasks = Task.objects.filter(user=user)
    return render(request, "ToDo/tasks.html", {
        "tasks" : tasks,
    })

def show_details(request, slug=None):
    if slug:
        task = get_object_or_404(Task, slug=slug)
    return render(request, "ToDo/task_details.html", {
        "task": task,
    })

def login_view(request):
    # if request.method == "POST":
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']
    #         user = authenticate(request, username=username, password=password)

    #     if not user:
    #         auth_login(request, user)
    #         return redirect("tasks")
    #     else:
    #         form.add_error(None, "Invalid username or password")
        
    # else:
    #     form = LoginForm()
    
    # return render(request, "ToDo/login.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("tasks")
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials."
            })
    return render(request, "ToDo/login.html")