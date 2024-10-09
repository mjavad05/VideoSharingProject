from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Rating, Video
from django.db.models import Avg


@receiver(post_save, sender=Comment)
def update_video_on_comment(sender, instance, created, **kwargs):
    if created:
        video = instance.video
        video.total_comments += 1
        video.save()


@receiver(post_save, sender=Rating)
def update_video_on_rating(sender, instance, created, **kwargs):
    if created:
        video = instance.video
        video.total_ratings += 1
        video.average_rating = Rating.objects.filter(video=video).aggregate(Avg('rating'))['rating__avg']
        video.save()
