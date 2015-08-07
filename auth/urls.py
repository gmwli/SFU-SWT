from django.conf.urls import patterns, url
#import views deleted this file
from django_cas import views


urlpatterns = patterns('',
    # ex /contactmanagment
    #url(r'^login/$', views.login, name='login'),
    url(r'^$', views.login, name='login'),
   	#url(r'^admin/$', views.login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page':'/succesfully_logged_out/'}),	
   # url(r'logout/$', 'django.contrib.auth.views.logout', name='logout'),
)


