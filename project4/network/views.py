from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from .models import UserProfile,User,UserPosts


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
        name = UserProfile.objects.filter(user = user).first()
        # - will make it reserved order
        allposts = UserPosts.objects.all().order_by('-timestamp')
        return render(request, "network/index.html",{"name" : name.firstname,"allposts":allposts,"trends":trends_result[0]["trends"]})
    except:
         return render(request, "network/login.html")
def post(request,id):
    user = request.user
    post = UserPosts.objects.filter(pk=id).first()
    likes = post.likes.all()
    return render(request, "network/post.html",{"post" : post,"likes" : likes,"trends":trends_result[0]["trends"]})

def profile(request):
    user = request.user
    profile = UserProfile.objects.filter(user = user).first()
    userposts = UserPosts.objects.filter(owner = user.profile).all().order_by('-timestamp')
    return render(request,"network/profile.html",{"userposts" : userposts,"name" : profile.firstname,"profile":profile,
    "trends":trends_result[0]["trends"]})

def other_profiles(request,username):
    user = User.objects.filter(username = username).first()
    profile = UserProfile.objects.filter(user = user).first()
    userposts = UserPosts.objects.filter(owner = user.profile).all()
    return render(request,"network/profile.html",{"userposts" : userposts,"name" : profile.firstname,"profile":profile,
    "trends":trends_result[0]["trends"]})

def twikat(request):
    return render(request,"network/tweetat.html")


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
        return render(request,"network/index")

def like(request, id):
        user = request.user
        post = UserPosts.objects.filter(pk = id).first()
        if 'liked' in request.GET:
            post.likes.delete(user)
            return HttpResponseRedirect('/twik')
        else:
            post.likes.add(user)
            return HttpResponseRedirect('/profile')

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
