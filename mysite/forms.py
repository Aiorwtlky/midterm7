from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'write', 'slug', 'category', 'intro', 'photolink', 'body']
        
class EditBookForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'write', 'slug', 'category', 'intro', 'photolink', 'body']
