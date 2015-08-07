from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'swt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^$', 'profiles.views.home'),
	(r'^login/', 'auth.django_cas.views.login'),
   #(r'^profiles/', include('profiles.urls')),
   # url(r'^getuser/', 'profiles.views.getUser'),
    url(r'^home/$', 'profiles.views.home'),
    url(r'^register/$', 'profiles.views.newProfile'),
    (r'^profiles/', include('profiles.urls')),
    url(r'^friends/$', 'profiles.views.home'),
    url(r'^friends/(?P<friend_id>\w+)/$', 'profiles.views.viewFriend'),
    (r'^workouts/', include('workouts.urls')),
    (r'^logintest/','auth.django_cas.views.logintest'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^logout/','auth.django_cas.views.logout',{'next_page':'/swt/'}),
    #(r'^reservation/',include('bookings.django_reservations.reservations.urls')),
    #url(r'^search/', include('bookings.urls')),
    #url(r'^reservations/', include('bookings_test.reservations.urls')),
   # url(r'^country/', include('bookings.urls')),
    #url(r'^booking/booking/',include('booking.urls')),
    url(r'^bookings/',include('bookings.urls')),
#    url(r'^image_test/',include('image_test.urls')),
)
