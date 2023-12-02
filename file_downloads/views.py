from django.views import View
from rest_framework.response import Response
from django.conf import settings
from file_uploads.models import UploadedFile
from rest_framework import status

from rest_framework.views import APIView

import jwt,datetime
from django.http import HttpResponse, HttpResponseBadRequest
from authentication.utils import get_authenticated_user
from django.conf import settings

class GenerateDownloadLinkView(APIView):
    def get(self, request, file_id):
        token = request.COOKIES.get('jwt', None)
        user = get_authenticated_user(token)
        print('user',user)
        if user is not None:
            if user.is_client:
                token_payload = {
                  'file_id': file_id,
                  'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
                 }
                secret_key = secret_key = settings.SECRET_KEY  
                download_token = jwt.encode(token_payload, secret_key, algorithm='HS256')
                # Construct the download link with the token as a query parameter
                download_link = f'{settings.FRONTEND_URL}/downloadfile/download/?token={download_token}'
                return Response({'message':'success','download_link': download_link},status=status.HTTP_201_CREATED)
            return Response({'message':'user should be client'},status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message':'Unauthenticated'})
    
class FileDownloadView(APIView):
    def get(self,request):
         # Get the token from the query parameters
     download_token = request.GET.get('token', None)
     user_token = request.COOKIES.get('jwt')
     

     if not download_token:
        return HttpResponseBadRequest('Token is missing')

     secret_key = secret_key = settings.SECRET_KEY

     try:
        # Verify and decode the token
        decoded_token = jwt.decode(download_token, secret_key, algorithms=['HS256'])
        file_id = decoded_token['file_id']
        user = get_authenticated_user(user_token)
        if user is not None:
          if not user.is_client:
             return Response({'message':'user is not client'},status=status.HTTP_401_UNAUTHORIZED)
          file_obj = UploadedFile.objects.get(id=file_id)

          # Serve the file for download
          with open(file_obj.file.path, 'rb') as file:
              response = HttpResponse(file.read(), content_type='application/octet-stream')
              response['Content-Disposition'] = f'attachment; filename="{file_obj.file.name}"'
              return response
     except jwt.ExpiredSignatureError:
        return HttpResponseBadRequest('Token has expired')
     except jwt.InvalidTokenError:
        return HttpResponseBadRequest('Invalid token')
     return HttpResponseBadRequest('Unauthenticated')
        
    
