from django.urls import path, include
from .views import blog_detail, blog_list, edit_blog, add_blog

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('edit_blog/<slug:slug>/', edit_blog, name='edit_blog'),
    path('add_blog/', add_blog, name='add_blog'),
    path('tinymce/', include('tinymce.urls')),
]
