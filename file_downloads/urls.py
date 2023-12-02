from django.urls import path
from .views import FileDownloadView, GenerateDownloadLinkView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   
    path('download/<int:file_id>', GenerateDownloadLinkView.as_view(), name='generate_download_link'),
    path('download/', FileDownloadView.as_view(), name='file_download'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)