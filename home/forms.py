from .models import Category, Post
from django import forms 

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        widget = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

