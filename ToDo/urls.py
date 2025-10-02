from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tasks", views.show_tasks, name="tasks"),
    path("task-toggle/<int:task_id>", views.task_toggle, name="task-toggle"),
    path("tasks/<int:task_id>", views.show_details, name="task_details"),
    path("signup", views.signup_view, name="signup"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("tasks-New", views.new_task, name="task-New"),
    path("task-delete/<int:task_id>", views.delete_task, name="task-delete"),
    path("task-redact/<int:task_id>", views.redact_task, name="task-redact"),
]
