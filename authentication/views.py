from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .utils import generate_registration_token, validate_registration_token
import jwt,datetime

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email=request.data['email']
        existing_user = CustomUser.objects.filter(email=email).first()
        if existing_user:
            re_registration_token = generate_registration_token(existing_user.email, existing_user.id)
            if not existing_user.is_active:
                #if the user is registered but not activated yet
                # Re-Send verification email
                subject = "Activate your account"
                message = f"Click the link to activate your account: {settings.FRONTEND_URL}/auth/activate/{re_registration_token}"
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [existing_user.email]
                send_mail(subject, message, from_email, to_email, fail_silently=False)
                return Response(
                    {"message": "Check your email for activation link."},
                    status=status.HTTP_200_OK,
                )
            #if the user is registered and activated
            return Response(
                    {"message": "user already registered"},
                    status=status.HTTP_409_CONFLICT,
                )
        # register new user
        serializer = UserSerializer(data=request.data)
       
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = serializer.save()
            registration_token = generate_registration_token(user.email, user.id)
            user.is_active = False
            # Send verification email
            subject = "Activate your account"
            message = f"Click the link to activate your account: {settings.FRONTEND_URL}/auth/activate/{registration_token}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.email]
            send_mail(subject, message, from_email, to_email, fail_silently=False)
            return Response(
                {
                    "message": "User registered successfully. Check your email for activation link."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):
    def get(self, request, token):
        return validate_registration_token(token)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):

        #if user is already logged in
        user_token = request.COOKIES.get('jwt',None)
        if user_token is not None:
            return Response({"message":"Already Logged in"},status=status.HTTP_400_BAD_REQUEST)
        
        #login user using jwt
        email = request.data.get("email")
        password = request.data.get("password")

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        
        #create the secret token for the user
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response()
        user_is = " "
        if user.is_superuser:
            user_is= "Operation User"
        else:
            user_is="client user"

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': f"logged in as {user_is} ",
        }
        return response

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
