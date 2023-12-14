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
    blogs = BlogPost.objects.order_by('-pk')

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
    meta_keywords = f"- {blog.keywords}"
    keywords = [
        item.strip()
        for item in blog.keywords.split(',')
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


def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'add_blog.html', {
                'form': BlogForm(),
                'success': True
            })
    else:
        form = BlogForm()
    return render(request, 'add_blog.html', {
        'form': BlogForm()
    })


@login_required(login_url='login')
def add_blog(request):
    user = request.user
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        cover_image = request.FILES.get(
            'cover_image')  # Get cover_image from FILES

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new']
            )
        else:
            category = None

        # Check if the 'publish' checkbox is checked
        is_published = 'publish' in data

        blog_post = BlogPost.objects.create(
            title=data['title'],
            author=user,
            summary=data['summary'],
            content=data['content'],
            category=category,
            is_published=is_published,
            youtube=data['youtube'],
            meta_keywords=data['meta_keywords'],
            meta_description=data['meta_description'],
            cover_image=cover_image,  # Use the cover_image from FILES
        )

        for image in images:
            blog_post.images.create(
                image=image, description=data.get('image_description'))

        return redirect('dashboard')

    context = {'categories': categories}
    return render(request, 'add_blog.html', context)
