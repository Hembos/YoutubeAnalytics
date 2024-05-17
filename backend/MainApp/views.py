import base64
import datetime
import threading

import jwt
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import transaction
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
import pytz

import settings.settings
from MainApp.serializers import *
from rest_framework import viewsets, permissions, status


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()


class IsValidated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_validated)


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    permission_classes = [IsValidated]
    serializer_class = ChannelSerializer


class ChannelGroupViewSet(viewsets.ModelViewSet):
    queryset = ChannelGroup.objects.all()
    permission_classes = [IsValidated]
    serializer_class = ChannelGroupSerializer


class VideoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsValidated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsValidated]
    serializer_class = CommentSerializer


class VideoGroupViewSet(viewsets.ModelViewSet):
    queryset = VideoGroup.objects.all()
    permission_classes = [IsValidated]
    serializer_class = VideoGroupSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    permission_classes = [IsValidated]
    serializer_class = RequestSerializer


class CalculationResultViewSet(viewsets.ModelViewSet):
    queryset = CalculationResult.objects.all()
    permission_classes = [IsValidated]
    serializer_class = CalculationResultSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        data = request.data
        response = Response()

        cookie = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'], None)

        if cookie is not None:

            try:
                token = RefreshToken(cookie)
            except TokenError as terror:
                return Response({"Error": str(terror)})
            user = User.objects.get(pk=token.payload['user_id'])
            token.blacklist()

        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=data["refresh"],
                    max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = {"token": data['access']}

                return response
            else:
                return Response({"No active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=data["refresh"],
                    max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = {"token": data['access']}

                return response
            else:
                return Response({"No active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)


class SignUp(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        with transaction.atomic():
            tz = pytz.timezone(settings.TIME_ZONE)
            data = request.data
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = serializer.data


            token = jwt.encode(
                {"user_email": user['email'], "exp": tz.localize(datetime.datetime.now()) + datetime.timedelta(hours=1)},
                settings.SECRET_KEY)

            current_site = get_current_site(request).domain

            relative_link = reverse('email-verify')
            absurl = 'http://' + current_site + relative_link + "?token=" + str(token)
            email_body = 'Hi ' + user['username'] + \
                         ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user['email'],
                    'email_subject': 'Verify your email'}

            Util.send_email(data=data)

            return Response(status=status.HTTP_201_CREATED)

class VerifyEmail(GenericAPIView ):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            print(payload)
            user = models.User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)