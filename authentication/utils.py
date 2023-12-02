import jwt
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.conf import settings
from .models import CustomUser
from rest_framework.exceptions import AuthenticationFailed


def generate_registration_token(email, user_id):
    payload = {
        "email": email,
        "user_id": user_id,
        "exp": datetime.utcnow()
        + timedelta(minutes=1),  # Token expiration time (adjust as needed)
        "iat": datetime.utcnow(),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def validate_registration_token(token):
    try:
        # Decode the token using the secret key
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        # Extract information from the payload
        email = payload.get("email")
        user_id = payload.get("user_id")

        # Check if the user exists
        user = CustomUser.objects.filter(id=user_id, email=email).first()

        if user:
            user.is_active = True
            user.is_client = True
            user.save()
            return Response(
                {"message": "registration_success"}, status=status.HTTP_201_CREATED
            )
        else:
            # Invalid token or user not found
            return Response(
                {"message": "Invalid registration link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except jwt.ExpiredSignatureError:
        # Token has expired
        return Response(
            {"message": "Registration link has expired."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except jwt.InvalidTokenError:
        # Invalid token
        return Response(
            {"message": "Invalid registration link."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
def get_authenticated_user(token):
    if not token:
        return None

    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      return None
    user = CustomUser.objects.filter(id=payload['id']).first()
 
    return user

