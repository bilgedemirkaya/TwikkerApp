
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile",views.profile,name="profile"),
    path("tweek",views.tweek,name= "tweek"),
    path("post/<int:id>",views.post,name="post"),
     path("post/<int:id>/like",views.like,name="like"),
    path("compose",views.twikat,name="twikat"),
    path("<str:username>",views.other_profiles,name="other_profiles"),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)