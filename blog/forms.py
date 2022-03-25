from django import forms
from .models import Blog, Comment, Topic, TComment
from home.models import WriterProfile

class BlogAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(BlogAddForm, self).__init__(*args, **kwargs)
        writer = self.request.user.writerprofile
        self.fields['writer'].queryset = WriterProfile.objects.filter(user = self.request.user)
    class Meta:
        model = Blog
        fields = ['category','writer','title','content']

class BlogEditForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['category','title','content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body' : forms.Textarea(attrs={
                'rows': '5',
                'cols': '40',
                'maxlength': '600',
            }),
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name','description']
        widgets = {
            'description' : forms.Textarea(attrs={
                'rows': '5',
                'cols': '40',
                'maxlength': '600',
            }),
        }

class TCommentForm(forms.ModelForm):
    class Meta:
        model = TComment
        fields = ['body']
        widgets = {
            'body' : forms.Textarea(attrs={
                'rows': '5',
                'cols': '40',
                'maxlength': '300',
            }),
        }