from django import forms
from .models import My_Task, My_Project, Comment


class CreateTask(forms.ModelForm):
    class Meta:
        model = My_Task
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={ 'class': 'form-control' }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 100%; height: 100px; resize: none;',
            })
        }


class CreateProject(forms.ModelForm):
    class Meta:
        model = My_Project
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={ 'class': 'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        labels = {
            'comment_text': ''
        }
        widgets = {
            'comment_text': forms.Textarea(attrs={
                 'class' : 'form-control',
                 'style': 'width: 100%; height: 100px; resize: none;',
                 'placeholder': 'Write a comment'})
        }