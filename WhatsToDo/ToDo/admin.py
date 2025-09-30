from django.contrib import admin
from .models import Task
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "completion", "creation_date")
    list_filter = ("completion",)
    search_fields = ("name", "user__user__username")  # search by Profile's User