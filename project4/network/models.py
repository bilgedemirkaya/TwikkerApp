from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', unique=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_image", blank=True,null=True)
    description = models.CharField(blank=True,max_length=100)
    city = models.CharField(max_length=64)
    firstname = models.CharField(max_length=64)

class UserPosts(models.Model):
    owner = models.ForeignKey(UserProfile,related_name='owner',on_delete=models.CASCADE)
    post = models.CharField(max_length=150)
    likes = models.ManyToManyField(User,related_name='likers',blank=True,null=True)
    timestamp = models.DateTimeField(auto_now=True)
    post_image = models.ImageField(blank=True,null=True,upload_to="post_image")