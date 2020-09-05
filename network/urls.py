
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
    path("explore",views.explore,name="explore"),
    path("tweek",views.tweek,name= "tweek"),
    path("directmessages",views.direct_message,name="direct_message"),
    path("loadbox",views.loadbox, name="loadbox"),
    path("inbox", views.inbox,name="inbox"),
    path("notifications",views.notifications,name="notifications"),
    path("sendmessage/<int:id>",views.sendit,name="sendit"),
    path("delete/<int:id>",views.delete,name="delete"),
    path("follow/<int:id>",views.follow, name ="follow"),
    path("post/<int:id>",views.post,name="post"),
    path("post/<int:id>/like",views.like,name="like"),
    path("<str:username>",views.other_profiles,name="other_profiles"),
    path("loadbox/<int:id>",views.onemessage,name="onemessage"),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)