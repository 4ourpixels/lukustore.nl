from django.urls import path, include
from .views import blog_detail, blog_list, edit_blog

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('<slug:tag_slug>/<slug:slug>/', blog_detail, name='blog_detail'),
    path('edit-blog/<slug:tag_slug>/<slug:slug>/', edit_blog, name='edit_blog'),
]
