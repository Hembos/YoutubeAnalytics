from django.shortcuts import render
from MainApp.serializers import *
from rest_framework import viewsets, permissions


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ChannelSerializer


class ChannelGroupViewSet(viewsets.ModelViewSet):
    queryset = ChannelGroup.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ChannelGroupSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VideoSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CommentSerializer


class VideoGroupViewSet(viewsets.ModelViewSet):
    queryset = VideoGroup.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VideoGroupSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RequestSerializer


class CalculationResultViewSet(viewsets.ModelViewSet):
    queryset = CalculationResult.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CalculationResultSerializer

