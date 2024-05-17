# Generated by Django 4.2.11 on 2024-05-17 23:16

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKeys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remaining_quota', models.IntegerField()),
                ('api_key', models.TextField()),
                ('mail', models.EmailField(max_length=254)),
                ('last_reset', models.DateTimeField()),
            ],
            options={
                'db_table': 'tb_api_keys',
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.TextField()),
                ('description', models.TextField()),
                ('published_at', models.DateTimeField()),
                ('subscriber_count', models.IntegerField()),
                ('title', models.TextField()),
                ('video_count', models.IntegerField()),
                ('view_count', models.IntegerField()),
            ],
            options={
                'db_table': 'tb_channel',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('duration', models.DurationField()),
                ('like_count', models.IntegerField()),
                ('published_at', models.DateTimeField()),
                ('view_count', models.IntegerField()),
                ('comment_count', models.IntegerField()),
                ('language', models.TextField()),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='video', to='MainApp.channel')),
            ],
            options={
                'db_table': 'tb_video',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_validated', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'tb_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='VideoGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='video_group', to=settings.AUTH_USER_MODEL)),
                ('videos', models.ManyToManyField(related_name='video_group', to='MainApp.video')),
            ],
            options={
                'db_table': 'tb_video_group',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField()),
                ('progress', models.IntegerField()),
                ('date_completion', models.DateTimeField()),
                ('data', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='request', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tb_request',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_text', models.TextField()),
                ('author_display_name', models.TextField()),
                ('like_count', models.IntegerField()),
                ('published_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('total_reply_count', models.IntegerField()),
                ('replies', models.ManyToManyField(to='MainApp.comment')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comment', to='MainApp.video')),
            ],
            options={
                'db_table': 'tb_comment',
            },
        ),
        migrations.CreateModel(
            name='ChannelGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('channel', models.ManyToManyField(related_name='channel_group', to='MainApp.channel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='channel_group', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tb_channel_group',
            },
        ),
        migrations.CreateModel(
            name='CalculationResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='calculation_result', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tb_calculation_result',
            },
        ),
    ]
