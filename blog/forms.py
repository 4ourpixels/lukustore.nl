from django import forms
from .models import BlogPost
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

# Create your tests here.


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ("__all__")
        exclude = ['created_at', 'slug', 'author',
                   'is_published', 'published_at', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Select category'}),
            'content': SummernoteWidget(),
            'summary': forms.Textarea(attrs={'class': 'form-control'}),
            'youtube': forms.Textarea(attrs={'class': 'form-control'}),
            'meta_keywords': forms.Textarea(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
