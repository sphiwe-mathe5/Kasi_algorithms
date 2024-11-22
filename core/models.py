from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    image = models.ImageField(upload_to='kasi_images', null=True, blank=True)
    url = models.URLField(max_length=200, unique=True ,null=True, blank=True)  
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class UserPostCount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Posts: {self.count}"

