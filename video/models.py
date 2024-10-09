from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(default=False)
    subscription_type = models.CharField(max_length=20, null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
    )


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    # video_url = models.URLField()
    upload_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=[('published', 'Published'), ('unpublished', 'Unpublished')])


class Subscription(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    type_subscription = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')])
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])


class WatchHistory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watch_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)