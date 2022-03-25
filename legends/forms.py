from django import forms
from .models import Legend, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']