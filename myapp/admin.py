from django.contrib import admin
from .models import My_Project, My_Task, Comment

admin.site.register(My_Project)
admin.site.register(My_Task)
admin.site.register(Comment)