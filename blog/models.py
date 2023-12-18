from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(unique=True, null=True, blank=True)
    youtube = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    cover_image = models.ImageField(
        null=True,
        blank=True,
        upload_to="blog/",
        default='blog.jpg'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def get_url(self):
        return reverse("blog_detail", kwargs={
            "slug": self.slug
        })

    @property
    def get_tags(self):
        return self.tags.all()


class BlogPhoto(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image_credit = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    blog = models.ForeignKey(
        BlogPost, on_delete=models.SET_NULL, null=True, blank=True)

    image = models.ImageField(
        null=False,
        blank=False,
        upload_to="blog/",
        default='image.jpg'
    )
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} | {self.blog.title}"
