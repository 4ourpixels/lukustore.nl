from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Category, Tag, BlogPost
from .forms import BlogForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def blog_list(request):
    title_tag = f"- Blogs"
    blogs = BlogPost.objects.filter(is_published=True)

    context = {
        'blogs': blogs,
        'title_tag': title_tag,
    }
    return render(request, 'blog_list.html', context)


def blog_detail(request, slug):
    blogs = BlogPost.objects.order_by('-pk')
    blog = get_object_or_404(BlogPost, slug=slug)
    title_tag = f"- {blog.title}"
    meta_description = f"- {blog.title}"
    meta_keywords = f"- {blog.meta_keywords}"
    keywords = [
        item.strip()
        for item in blog.meta_keywords.split(',')
        if item.strip()
    ]

    # Retrieve photos from the category named "SS23"
    category_ss23 = Category.objects.get(name='SS23')

    context = {
        'blog': blog,
        'title_tag': title_tag,
        'blogs': blogs,
        'keywords': keywords,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'category_ss23': category_ss23,
    }
    return render(request, 'blog_detail.html', context)


def edit_blog(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    title_tag = f"- Update: {blog.title}"

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)

        if form.is_valid():
            form.save()
            return render(request, 'edit_blog.html', {
                'form': form,
                'success': True
            })
        else:
            print("Errors occurred while uploading: ",
                  form.errors)
    else:
        form = BlogForm(instance=blog)

    context = {
        'form': form,
        'title_tag': title_tag,
        'blog': blog,
    }

    return render(request, 'edit_stock.html', context)


@login_required(login_url='login')
def add_blog(request):
    title_tag = "Add new blog"

    if request.method == 'POST':
        new_blog_form = BlogForm(request.POST)
        if new_blog_form.is_valid():
            new_blog = new_blog_form.save(commit=False)
            # Assuming you have a ForeignKey to User in your Blog model
            new_blog.author = request.user
            new_blog.save()
            return render(request, 'add_blog.html', {
                'form': BlogForm(),
                'success': True
            })
    else:
        new_blog_form = BlogForm()

    context = {
        'title_tag': title_tag,
        'new_blog_form': new_blog_form
    }

    return render(request, 'add_blog.html', context)
