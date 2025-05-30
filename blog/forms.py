# blog/forms.py

from django import forms
from .models import Post
from .models import Comment
from taggit.forms import TagWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body',]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-600'
            }),
            'body': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-600 h-40'
            }),
        }


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-md border border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 p-3 text-gray-700',
                'placeholder': 'Your name',
            }),
            'body': forms.Textarea(attrs={
                'class': 'w-full rounded-md border border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 resize-y min-h-[120px] p-3 text-gray-700',
                'placeholder': 'Write something interesting ;P',
                'rows': 5,
            }),
        }


