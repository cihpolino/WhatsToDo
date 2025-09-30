from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Task
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    return render(request, "ToDo/index.html")

def show_tasks(request):
    user = User.objects.get(username = "chipolino")
    task = Task.objects.get(user=user)
    return render(request, "ToDo/tasks.html", {
        "task" : task,
    })

def show_details(request, slug=None):
    if slug:
        task = get_object_or_404(Task, slug=slug)
    return render(request, "ToDo/task_details.html", {
        "task": task,
    })