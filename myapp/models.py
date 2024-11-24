"""modelos"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class My_Project(models.Model):
    """proyectos"""
    name = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.name)

class My_Task(models.Model):
    """Tareas"""
    title = models.CharField(max_length=25)
    description = models.TextField()
    project = models.ForeignKey(My_Project, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)

    """establecer nombre"""
    def __str__(self) -> str:
        return f"{self.title}  ->  {self.project.name}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)

    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()
    
    def __str__(self) -> str:
        return f"{self.user}"


