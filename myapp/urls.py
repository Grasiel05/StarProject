"""archivo principal de las urls"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.initial, name='home'),
    path('about/', views.about, name='about' ),
    path('projects/<int:user_id>', views.projects, name='projects'),
    path('projects/tasks-undone/<int:p_id>/', views.project_detail, name='project_detail'),
    path('projects/tasks-done/<int:p_id>/', views.project_detail, name='tasks_done'),
    path('create_task/<int:project_id>/', views.create_task, name='create_task'),
    path('create_project/<int:user_id>', views.create_project, name='create_project'),
    path('tasks/done/<int:task_id>/<int:project_id>/', views.mark_task, name='mark_task'),
    path('tasks/not_done/<int:task_id>/<int:project_id>/', views.unmark_task, name='unmark_task'),
    path('projects/delete_project/<int:p_id>/<int:user_id>/', views.delete_project, name="delete_project"),
    path('tasks/delete_task/<int:id_project>/<int:t_id>/<str:url>/', views.delete_task, name="delete_task"),
    path('tasks/<int:p_id>/<int:t_id>/', views.task_detail, name="task_detail"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.logear, name='login'),
    path('logout/', views.deslogear, name='logout'),
    path('like/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('dislike/<int:comment_id>/', views.dislike_comment, name='dislike_comment'),
]