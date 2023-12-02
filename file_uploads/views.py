from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UploadedFileSerializer
from authentication.utils import get_authenticated_user
from file_uploads.models import UploadedFile
from django.http import JsonResponse
from django.db import DatabaseError
import pandas as pd

class FileUploadView(APIView):
    parser_classes = (MultiPartParser,FormParser)

    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        user = get_authenticated_user(token)
        if not user.is_superuser:
            return Response({"detail": "Permission denied. Only superusers can upload files."},
                            status=status.HTTP_401_UNAUTHORIZED)
        file_serializer = UploadedFileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class FileListView(APIView):
    def get(self, request):
        user_token = request.COOKIES.get('jwt',None)
        if user_token is None:
            return Response({"message":"Login first to display data"},status=status.HTTP_401_UNAUTHORIZED)
        try:
          files = UploadedFile.objects.all()
          df = pd.DataFrame.from_records(files.values())
          file_data = df[['id', 'file']]
          json_data = file_data.to_dict(orient='records')
          print(json_data)
          return JsonResponse({"file_data":json_data}, safe=False)
        except DatabaseError as e:
            return Response({e},status=status.HTTP_400_BAD_REQUEST)