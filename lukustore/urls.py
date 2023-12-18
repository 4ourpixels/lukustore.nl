from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("myapp.urls")),
    path('blog/', include('blog.urls')),
    path('summernote/', include('django_summernote.urls')),
]
# Configure admin titles
admin.site.site_header = "Luku Store.nl Admin"

# Tab/Site Title
admin.site.site_header = "Luku Store.nl"

admin.site.index_title = "Luku Store.nl - Admin"
