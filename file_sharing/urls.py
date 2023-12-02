from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentication.urls")),
    path("api/file/", include("file_uploads.urls")),
    path("api/downloadfile/",include("file_downloads.urls"))
]
