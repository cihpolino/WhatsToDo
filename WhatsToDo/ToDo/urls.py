from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tasks", views.show_tasks, name="tasks"),
    path("tasks/<slug:slug>", views.show_details, name="task_details"),
]
