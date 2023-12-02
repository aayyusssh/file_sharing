from django.urls import path
from .views import FileUploadView, FileListView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload', FileUploadView.as_view(), name='file-upload'),
     path("list", FileListView.as_view(), name="list"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)