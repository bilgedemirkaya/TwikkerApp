from django.contrib import admin
from .models import UserProfile,UserPosts,Follower,LikedPost,DirectMessageClass

admin.site.register(UserProfile)
admin.site.register(UserPosts)
admin.site.register(Follower)
admin.site.register(LikedPost)
admin.site.register(DirectMessageClass)

