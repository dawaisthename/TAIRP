import re
from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user=models.IntegerField(default=1)
    bio = models.TextField(blank=True)
    profileimg=models.ImageField(default='default.jpg',upload_to='profile_images')
    location=models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.CharField(max_length=255)
    image=models.ImageField(upload_to='Post_images')
    caption=models.TextField()
    created_at =models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)
    def __str__(self):
        return self.user
class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.PROTECT)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    commented_at= models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.username
class LikePost(models.Model):
    post_id=models.CharField(max_length=50)
    username=models.CharField(max_length=50)

    def __str__(self):
        return self.username
class FollowersCount(models.Model):
    follower=models.CharField(max_length=255)
    user=models.CharField(max_length=255)

    def __str__(self):
        return self.user