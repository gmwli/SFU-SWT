from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^$', views.myProfile, name='myProfile'),
    url(r'^new/$', views.newProfile, name='newProfile'),
    url(r'^edit/$', views.editProfile, name='editProfile'),
    url(r'^friend-request/$', views.requestFriend, name='requestFriend'),
    url(r'^friend-accept/(?P<friend_id>\w+)/$', views.acceptFriend, name='acceptFriend'),
    url(r'^friend-decline/(?P<friend_id>\w+)/$', views.declineFriend, name='declineFriend'),
    url(r'^friend-delete/(?P<friend_id>\w+)/$', views.deleteFriend, name='deleteFriend'),
	url(r'^friends/$', views.home, name='home'),
	url(r'^friends/(?P<friend_id>\w+)/$', views.viewFriend, name='viewFriend'),
)

