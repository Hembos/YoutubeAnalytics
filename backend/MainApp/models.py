from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Channel(models.Model):
    country = models.TextField()
    description = models.TextField()
    published_at = models.DateTimeField()
    subscriber_count = models.IntegerField()
    title = models.TextField()
    video_count = models.IntegerField()
    view_count = models.IntegerField()

    class Meta:
        db_table = 'tb_channel'


class ChannelGroup(models.Model):
    title = models.TextField()
    channel = models.ManyToManyField(Channel, related_name="channel_group")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="channel_group")

    class Meta:
        db_table = 'tb_channel_group'


class Video(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.DO_NOTHING, related_name="video")
    description = models.TextField()
    duration = models.DurationField()
    like_count = models.IntegerField()
    published_at = models.DateTimeField()
    view_count = models.IntegerField()
    comment_count = models.IntegerField()
    language = models.TextField()

    class Meta:
        db_table = 'tb_video'


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.DO_NOTHING, related_name="comment")
    original_text = models.TextField()
    author_display_name = models.TextField()
    like_count = models.IntegerField()
    published_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    total_reply_count = models.IntegerField()
    replies = models.ManyToManyField('self')

    class Meta:
        db_table = 'tb_comment'


class VideoGroup(models.Model):
    title = models.TextField()
    videos = models.ManyToManyField(Video, related_name="video_group")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="video_group")

    class Meta:
        db_table = 'tb_video_group'


class Request(models.Model):
    type = models.IntegerField()
    progress = models.IntegerField()
    date_completion = models.DateTimeField()
    data = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="request")

    class Meta:
        db_table = 'tb_request'


class CalculationResult(models.Model):
    result = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="calculation_result")

    class Meta:
        db_table = 'tb_calculation_result'


class User(AbstractUser):
    is_validated = models.BooleanField(default=False)

    class Meta:
        db_table = "tb_user"

class ApiKeys(models.Model):
    remaining_quota = models.IntegerField()
    api_key = models.TextField()
    mail = models.EmailField()
    last_reset = models.DateTimeField()

    class Meta:
        db_table = "tb_api_keys"