from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager

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
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']


    def get_absolute_url(self):
     return reverse('blog:post_detail', args=[
        self.publish.year,
        self.publish.month,
        self.publish.day,
        self.slug
    ])

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
            return f'Comment by {self.name}'