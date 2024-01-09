from django.urls import path
from .views import blog_detail, blog_list, edit_blog, ss23

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('<slug:tag_slug>/<slug:slug>/', blog_detail, name='blog_detail'),
    path('luku-store-nl/ss23-luku-book/', ss23, name='ss23'),
    path('edit-blog/<slug:tag_slug>/<slug:slug>/', edit_blog, name='edit_blog'),
]
