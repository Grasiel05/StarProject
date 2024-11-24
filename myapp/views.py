"""Modulo donde se definen las urls"""
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreateTask, CreateProject, CommentForm
from .models import My_Project, My_Task, Comment
from .decorators import unauthenticated_user

# Create your views here.
def initial(request):
    """index page"""
    comments = Comment.objects.all()

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.save()
                return redirect('home')
        else:
            form = CommentForm()
            return render(request, 'index.html', {
            'comments': comments,
            'form': form,
            'error': 'Please Log in to comment'
        })
    else:
        form = CommentForm()
        return render(request, 'index.html', {
            'comments': comments,
            'form': form,
        })

def about(request):
    """url para mostrar about"""
    return render(request, 'about.html')

@login_required
def projects(request, user_id):
    """projects page"""
    p = list(My_Project.objects.filter(user_id=user_id))
    if len(p) == 0:
        return render(request, 'projects/projects.html', {
            'alert' : "You don't have any project",
            'user_id': user_id
        })
    if len(p) > 1:
        p.reverse()

    return render(request, 'projects/projects.html', {
        'projects' : p
    })

@login_required
def create_project(request, user_id):
    """funcion para el formulario de crear proyectos"""
    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {
            'form': CreateProject()
        })
    else:
        My_Project.objects.create(name=request.POST['name'], user_id=user_id)
        return redirect('projects', user_id)

@login_required
def mark_task(request, task_id, project_id):
    """marcar una tarea como hecha"""
    if request.method == "POST":
        task = get_object_or_404(My_Task, id = task_id)
        task.done = 1
        task.save()
        return redirect('project_detail' , str(project_id))
    else:
        return redirect('project_detail' , str(project_id))


@login_required
def unmark_task(request, task_id, project_id):
    """marcar una tarea como no hecha"""
    if request.method == "POST":
        task = get_object_or_404(My_Task, id = task_id)
        task.done = 0
        task.save()
        return redirect('tasks_done' , str(project_id))
    else:
        return redirect('tasks_done' , str(project_id))

@login_required
def create_task(request, project_id):
    """funcion para el formulario de crear tareas"""
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {
        'form': CreateTask()
        })
    else:
        My_Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            project_id=project_id)
        return redirect('project_detail' , str(project_id))

@login_required
def project_detail(request, p_id):
    print(request)
    """mmuestra las tareas de un proyecto"""
    project = get_object_or_404(My_Project, id=p_id)
    tasks_list = My_Task.objects.filter(project_id=p_id)
    if request.path == '/projects/tasks-undone/' + str(p_id) + '/':
        tasks_not_done = list(tasks_list.filter(done = 0))
        tasks_not_done.reverse()
        return render(request, 'projects/detail.html', {
            'project': project,
            'tasks_not_done': tasks_not_done,
            'url': 'undone'
        })
    else:
        tasks_done = list(tasks_list.filter(done = 1))
        tasks_done.reverse()
        return render(request, 'projects/detail.html', {
            'project': project,
            'tasks_done': tasks_done,
            'url': 'done'
        })

@login_required
def delete_project(request, p_id, user_id):
    """borrar un proyecto"""
    project = My_Project.objects.get(id=p_id)
    if request.method == 'POST':
        project.delete()
        return redirect('projects', user_id)
    return redirect('projects', user_id)

@login_required
def delete_task(request, id_project, t_id, url):
    """borrar una tarea"""
    task = My_Task.objects.get(id=t_id)
    if request.method == 'POST':
        print(request.path)
        task.delete()
        return redirect('project_detail', p_id=id_project) if url == 'undone' else redirect('tasks_done', p_id=id_project)
    return redirect('project_detail', p_id=id_project) if url == 'undone' else redirect('tasks_done', p_id=id_project)

@login_required
def task_detail(request,p_id, t_id):
    """informacion sobre una tarea"""
    task = get_object_or_404(My_Task, id=t_id)
    task_description = task.description
    return render(request, 'tasks/task_detail.html', {
        'task_description': task_description,
        'p_id': p_id
    })


@unauthenticated_user
def signup(request):
    """funcion para registrarse"""
    if request.method == "GET":
        return render(request, 'signup.html', {
            'form': UserCreationForm(),
        })
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"])
                user.save()
                login(request, user)
                messages.success(request, 'User created succesfuly')
                return redirect('home')
            except IntegrityError:
                messages.error(request, 'User already exist')
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                })
        messages.error(request, 'Passwords do not match')
        return render(request, 'signup.html', {
            'form': UserCreationForm(),
        })

@unauthenticated_user
def logear(request):
    """funcion para iniciar sesion"""
    if request.method == "GET":
        return render(request, 'logear.html', {
        'form': AuthenticationForm()
        })
    else:
        user = authenticate(request,
                            username=request.POST["username"],
                            password= request.POST["password"])
        if user is None:
            messages.error(request, "User or Password are incorrect")
            return render(request, 'logear.html', {
                'form': AuthenticationForm(),
            })
        else:
            login(request, user)
            return redirect('home')

@login_required
def deslogear(request):
    """funcion para deslogear a un usuario"""
    logout(request)
    return redirect('home')

def like_comment(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
            if request.user in comment.dislikes.all():
                comment.dislikes.remove(request.user)
        return redirect('home')
    else:
        comments = Comment.objects.all()
        form = CommentForm()
        return render(request, 'index.html', {
            'comments': comments,
            'form': form,
            'error': 'You must be logged in to react, please login first'
        }) 
    

def dislike_comment(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.dislikes.all():
            comment.dislikes.remove(request.user)
        else:
            comment.dislikes.add(request.user)
            if request.user in comment.likes.all():
                comment.likes.remove(request.user)
        return redirect('home')
    else:
        comments = Comment.objects.all()
        form = CommentForm()
        return render(request, 'index.html', {
            'comments': comments,
            'form': form,
            'error': 'You must be logged in to react, please login first'
        })