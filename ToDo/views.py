from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import logging
from .forms import redactForm
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
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

def show_details(request, slug=None):
    if slug:
        task = get_object_or_404(Task, slug=slug)
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
            return render(request, "users/login.html", {
                "message": "Invalid credentials."
            })
    return render(request, "ToDo/login.html")

def logout_view(request):
    logout(request)
    return render(request, "ToDo/logout.html")

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #creates a user
            login(request, user)
            return HttpResponseRedirect(reverse("tasks"))
    else:
        form = UserCreationForm()

    return render(request, "ToDo/signup.html", {
        "form": form
    })

        # firs_name = request.POST.get("firs_name")
        # last_name = request.POST.get("last_name")
