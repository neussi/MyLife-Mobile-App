import firebase_admin
from firebase_admin import auth, credentials
from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.conf import settings
import os

User = get_user_model()

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        id_token = auth_header.split(' ').pop()

        # Handle Mock Token for Development
        if settings.DEBUG and id_token == 'mock_token':
            uid = 'mock_uid'
            email = 'mock@example.com'
        else:
            try:
                # Initialize Firebase App if not already initialized
                # In production, credentials should be loaded from secure path or env
                if not firebase_admin._apps:
                    cred_path = getattr(settings, 'FIREBASE_CREDENTIALS_PATH', None)
                    if cred_path and os.path.exists(cred_path):
                        cred = credentials.Certificate(cred_path)
                        firebase_admin.initialize_app(cred)
                    else:
                        # Fallback for dev/test without creds or implicit environment auth
                        # This might fail if no creds are found
                        try:
                            firebase_admin.get_app()
                        except ValueError:
                             firebase_admin.initialize_app()

                decoded_token = auth.verify_id_token(id_token)
                uid = decoded_token.get('uid')
                email = decoded_token.get('email')
            except Exception as e:
                # Return None to allow other authentication classes (or AllowAny) to proceed
                # raising AuthenticationFailed blocks AllowAny
                return None

        try:
            user = User.objects.get(firebase_uid=uid)
        except User.DoesNotExist:
            # Create user if not exists (Auto-signup)
            # We use the email/uid as username fallback
            username = email if email else uid
            user, created = User.objects.get_or_create(username=username, defaults={
                'email': email,
                'firebase_uid': uid
            })
            if created:
                user.set_unusable_password()
                user.save()

        return (user, None)
