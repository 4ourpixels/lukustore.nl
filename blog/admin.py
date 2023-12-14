from django.contrib import admin
from .models import BlogPost, Category, Tag
# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Tag)
admin.site.register(Category)

admin.site.site_header = "Luku Store.nl Admin"

# Tab/Site Title
admin.site.site_header = "Luku Store.nl"

admin.site.index_title = f"Luku Store.nl - Blogs"
