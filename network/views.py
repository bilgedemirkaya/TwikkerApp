import time
import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from random import randint
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F


from .models import UserProfile,User,UserPosts,Follower,LikedPost,DirectMessageClass

import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("ifVXfIz1sKVlhh0QuLB5Gxtjk", "kBoO6b4IEMK4flshXRTbnfAt1BkTIsy7Tk3tYrrHE61CYsucld")
auth.set_access_token("349648130-UMevpz1wGP8KJ2RlHro73Zb9VDijIpsAg2GrnxC2", "yGlFC9ably9Q18uQQMl4Tr9oqs12R8hKEtvR4pu4Eu2DF")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

trends_result = api.trends_place(1)[:10]


def index(request):
    try:
        user = request.user
        # - will make it reserved order
        allposts = UserPosts.objects.all().order_by('-timestamp')
        return render(request, "network/index.html",{"name" : user.profile.firstname,"allposts":allposts,
        "trends":trends_result[0]["trends"]})
    except:
         return render(request, "network/login.html")

def post(request,id):
    # show the post details
    user = request.user
    post = UserPosts.objects.filter(pk=id).first()
    likes = post.likes.all()
    is_like = post.likes.filter(id=user.id).exists()
    return render(request, "network/post.html",{"post" : post,"likes" : likes,"trends":trends_result[0]["trends"],
    "name" : user.profile.firstname,"is_liked":is_like})


def profile(request):
    # show the profile page
    user = request.user
    userposts = UserPosts.objects.filter(owner = user.profile).all().order_by('-timestamp')
    profile = UserProfile.objects.filter(user = user).first()
    following = user.following.all()
    followers = user.followers.all()
    likedposts = LikedPost.objects.filter(liker = user).all()
    return render(request,"network/profile.html",{"userposts" : userposts,"name" : user.profile.firstname,"likedposts":likedposts,
    "profile":profile,"followers":followers,"following":following,"trends":trends_result[0]["trends"]})

@csrf_exempt
def direct_message(request):
    
    # Composing a new message must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    currentuser=request.user
    data = json.loads(request.body)
    username = data.get("receiver")
    receiver = User.objects.filter(username=username).first()

    # Get contents of message
    content = data.get("content", "")
    
    # send a message
    prev_contents = DirectMessageClass.objects.filter(sender=currentuser,receiver=receiver).all()
    prev_contents.create(sender=currentuser,receiver=receiver,content=content)
    
       
    return JsonResponse({"message": "message sent successfully."}, status=201)

def loadbox(request):
    user = request.user 
    # Return messages in reverse chronologial order
    messages = DirectMessageClass.objects.filter(receiver=user).order_by("-timestamp").all()
    return JsonResponse(
        [
            *[message.serialize() for message in messages],
        ],
        safe=False
    )

def inbox(request):
    user = request.user
    return render(request,"network/inbox.html",{"name" : user.profile.firstname,
        "trends":trends_result[0]["trends"],"user":user})

@csrf_exempt
def onemessage(request,id):

    # Query for one message
    try:
        message = DirectMessageClass.objects.get(pk=id)
        sender = message.sender
        receiver = message.receiver
        replies = DirectMessageClass.objects.filter(sender=receiver,receiver=sender).all()
        
    except:
        return JsonResponse({"error": "Message not found."}, status=404)

    # Return message contents
    if request.method == "GET":   
        d = {"replies":[reply.content for reply in replies]}.copy()
        d.update({"senderimage":message.sender.profile.image.url,"sendername":message.sender.profile.firstname,"sender":message.sender.username,
        "content":message.content})
        return JsonResponse(d,safe=False)

    # Update whether message is read
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("read") is not None:
            message.read = data["read"]
        message.save()
        return HttpResponse(status=204)

    # Message must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
def sendit(request,id):
    if request.method == "POST":
        receiver = User.objects.filter(pk=id).first()
        username =receiver.username
        sender = request.user
        content = request.POST['content']
        # save the message in database
        DirectMessageClass.objects.create(sender=sender,receiver=receiver,content=content)
        messages.add_message(request,messages.SUCCESS,"Message sent")
        return HttpResponseRedirect(reverse('other_profiles',args=[str(username)]))
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

def other_profiles(request,username):
        # other users profiles
        currentuser = request.user
        user = User.objects.filter(username = username).first()
        prf = UserProfile.objects.filter(user = user).first()
        following = user.following.all()
        followers = user.followers.all()
        userposts = UserPosts.objects.filter(owner = user.profile).all().order_by("-timestamp")
        is_following = Follower.objects.filter(following = user, follower = currentuser).exists()
        likedposts = LikedPost.objects.filter(liker = user).all()
        return render(request,"network/otherprofile.html",{"userposts" : userposts,"name" : request.user.profile.firstname,"is_following":is_following,
        "followers":followers,"following":following,"likedposts":likedposts,"profile":prf,"trends":trends_result[0]["trends"]})


def follow(request,id):
    currentuser = request.user
    user = User.objects.filter(id=id).first()
    followingRel = Follower.objects.filter(following = user, follower = currentuser).first()
    if followingRel:
        followingRel.delete()
        return HttpResponseRedirect(reverse('other_profiles',args=[str(user.username)]))
        
    else:
        if user == currentuser:
            messages.add_message(request,messages.ERROR,'You cannot follow yourself')
            return HttpResponseRedirect(reverse('other_profiles',args=[str(user.username)]))
        else:
            Follower.objects.create(following = user, follower = currentuser)
            return HttpResponseRedirect(reverse('other_profiles',args=[str(user.username)]))

def notifications(request):
    user = request.user
    following = user.following.all()
    followers = user.followers.all()
    userposts = UserPosts.objects.filter(owner=user.profile).all()
    liked = LikedPost.objects.filter(postowner=user).all()
    return render(request,"network/notifications.html",{"name" : user.profile.firstname,"liked":liked,
    "followers":followers,"following":following,"trends":trends_result[0]["trends"],"userposts":userposts})

def tweek(request):
    if request.method == "POST":
        user = request.user
        post = request.POST["post"]
        try:
            post_image = request.FILES["image"]
            fs = FileSystemStorage()
            filename = fs.save(post_image.name, post_image)
            UserPosts.objects.create(owner = user.profile,post = post, post_image = filename)
            messages.add_message(request,messages.SUCCESS,'Tweek Sent')
        except:
            UserPosts.objects.create(owner = user.profile,post = post)
            messages.add_message(request,messages.SUCCESS,'Tweek Sent')
        
        return HttpResponseRedirect('/')
    else:
        return render(request,"network/index.html")

def like(request, id):
    user = request.user
    post = UserPosts.objects.filter(pk = id).first()
    is_liked = post.likes.filter(id=user.id).exists()
    if is_liked: # If liked before
        post.likes.remove(user)
        return HttpResponseRedirect(reverse('post',args=[str(id)]))
    else:
        post.likes.add(user)
        LikedPost.objects.create(post=post, liker = user,postowner = post.owner.user)
        return HttpResponseRedirect(reverse('post',args=[str(id)]))

def explore(request):
    user = request.user
    count = UserProfile.objects.count()
    profiles = UserProfile.objects.all().order_by('?')[0:3]


    return render(request, "network/explore.html",{"name" : user.profile.firstname,"profiles":profiles,
        "trends":trends_result[0]["trends"]})

@csrf_exempt
def delete(request,id):
    if request.method == "POST":
        
        will_delete = UserPosts.objects.filter(id=id)
        will_delete.delete()
        messages.add_message(request,messages.SUCCESS,"Post deleted")
        return HttpResponseRedirect('/')
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


        
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        city = request.POST["city"]
        description = request.POST["description"]
        try:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
        except:
            filename = 'profile_image/egg.jpg'

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        UserProfile.objects.create(user = user, city=city,firstname=firstname,description = description,image = filename) 
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
