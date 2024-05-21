import re

from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
import urllib.parse

import settings.settings
from MainApp.serializers import *
from rest_framework import viewsets, permissions, status


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
        response = Response()

        cookie = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'], None)
        user = None
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
                return Response({"No active": "This account is not active!!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_400_BAD_REQUEST)


class SignUp(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        with transaction.atomic():
            data = request.data
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = serializer.data

            absurl = 'http://' + get_current_site(request).domain + reverse('email-verify')
            params = {'email': user['email'], 'token': user['token']}
            url = absurl + '?' + urllib.parse.urlencode(params)
            email_body = 'Hi ' + user['username'] + ',\nUse the link below to verify your email \n' + url
            send_mail('Verify your email', email_body, None, [user['email']], False, )

            return Response({"success": "Account successfully created"}, status=status.HTTP_201_CREATED)


class VerifyEmail(GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.GET.get('token')
        email = request.GET.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

        if not token == user.token:
            return Response({'error': 'Invalid token'}, status.HTTP_400_BAD_REQUEST)

        if user.is_verified:
            return Response({'error': 'User already verified'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_verified = True
            user.save()

        return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)


class SendVerificationLink(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.is_verified:
            return Response({'error': 'User already verified'}, status=status.HTTP_400_BAD_REQUEST)

        absurl = 'http://' + get_current_site(request).domain + reverse('email-verify')
        params = {'email': request.user.email, 'token': request.user.token}
        url = absurl + '?' + urllib.parse.urlencode(params)
        email_body = 'Hi ' + request.user.username + ',\nUse the link below to verify your email \n' + url
        send_mail('Verify your email', email_body, None, [request.user.email], False)

        return Response(status=status.HTTP_200_OK)


def get_youtube_video_id(url):
    video_id = None

    pattern = r"^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"

    match = re.search(pattern, url)
    if match:
        video_id = match.group(7)
    return video_id


class MakeDownloadRequest(GenericAPIView):
    permission_classes = [IsValidated]

    def post(self, request):
        url = request.POST.get('url', None)
        yt_id = request.POST.get('id', None)
        request_type = request.POST.get('request_type', None)

        if yt_id is not None:
            return Response()

        if url is not None:
            yt_id = get_youtube_video_id(url)
            return Response()

        return Response()
