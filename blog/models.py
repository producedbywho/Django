from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Status(models.TextChoices):
    DRAFT = 'DF', 'Draft'
    PUBLISHED = 'P', 'Published'

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length = 134)
    slug = models.SlugField(default = "", null = False)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(choices = Status.choices, default = Status.DRAFT)

    class Meta:
        ordering = ['-publish']
