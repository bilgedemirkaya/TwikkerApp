from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', unique=True,
                                 on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_image", blank=True,null=True)
    description = models.CharField(blank=True,max_length=100)
    city = models.CharField(max_length=64)
    firstname = models.CharField(max_length=64)



class UserPosts(models.Model):
    owner = models.ForeignKey(UserProfile,related_name='owner',
                                        on_delete=models.CASCADE)
    post = models.CharField(max_length=150)
    likes = models.ManyToManyField(User,related_name='likers',
                                        blank=True,null=True)
    timestamp = models.DateTimeField(auto_now=True)
    post_image = models.ImageField(blank=True,null=True,
                                    upload_to="post_image")

class LikedPost(models.Model):
    postowner = models.ForeignKey(User,related_name="postowner",on_delete=models.CASCADE,null=True,blank=True)
    post = models.ForeignKey(UserPosts,related_name="likedpost",
                            on_delete=models.CASCADE)
    liker = models.ForeignKey(User,related_name="liked",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} is liked {}'.format(self.liker, self.post)

class Follower(models.Model):

    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='followers')
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        """
        A User can of follow or be following another User once.
        """
        unique_together = ('follower', 'following')

    def __str__(self):
        return '{} is followed by {}'.format(self.follower, self.following)

class DirectMessageClass(models.Model):  
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='from_this')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='to_this')
    timestamp = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=200)
    read = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "sendername":self.sender.profile.firstname,
            "senderimage":self.sender.profile.image.url,
            "receiver": self.receiver.username,
            "content": self.content,
            "timestamp":self.timestamp.strftime("%m/%d/%Y, %H:%M:%S"), # to format date
            "read":self.read,
        }
        def __str__(self):
            return '{}send message to {}'.format(self.sender.username, self.receiver.username)
