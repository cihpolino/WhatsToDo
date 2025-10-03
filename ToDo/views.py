from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import logging
from .forms import redactForm, CustomUserCreationForm
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("tasks"))
    else:
        return render(request, "ToDo/index.html")

def show_tasks(request):
    user = request.user
    tasks = Task.objects.filter(user=user)
    # get name of the user
    first_name = user.first_name
    last_name = user.last_name
    return render(request, "ToDo/tasks.html", {
        "tasks" : tasks,
        "first_name": first_name,
        "last_name": last_name
    })

def show_details(request, task_id=None):
    if task_id:
        task = Task.objects.get(id=task_id)
    return render(request, "ToDo/task_details.html", {
        "task": task,

    })

def login_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("tasks")
        else:
            return render(request, "ToDo/login.html", {
                "message": "Invalid username or password."
            })
    return render(request, "ToDo/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
    # return render(request, "ToDo/logout.html")

def new_task(request):
    # Take info
    if request.method == "POST":
        user = request.user
        name = request.POST['name']
        description = request.POST['description']
        # create task
        Task.objects.create(user=user, name=name, description=description)
        return HttpResponseRedirect("tasks")
    return render(request, "ToDo/New.html")

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return HttpResponseRedirect("/tasks")

def redact_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method =="POST":
        name = request.POST["name"]
        description = request.POST["description"]
        task.name = name
        task.description = description
        task.save()
        return HttpResponseRedirect(reverse("tasks"))
    
    form = redactForm(initial={"name": f"{task.name}", "description": f"{task.description}"})
    return render(request, "ToDo/task_redact.html", {
        "form": form,
        "task": task,
    })

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #creates a user
            login(request, user)
            return HttpResponseRedirect(reverse("tasks"))
    else:
        form = CustomUserCreationForm()

    return render(request, "ToDo/signup.html", {
        "form": form
    })

def task_toggle(request, task_id):
    if request.method == "POST":
        task = Task.objects.get(id=task_id)
        status = request.POST.get("status")
        task.completion = bool(status)
        task.save()
        return HttpResponseRedirect(reverse("tasks"))
