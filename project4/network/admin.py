from django.contrib import admin
from .models import UserProfile,UserPosts

admin.site.register(UserProfile)
admin.site.register(UserPosts)

