from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
  #  url(r'^$', views.showOptions, name='showOptions'),
    url(r'^$',views.BookMachine, name='BookMachine'),
#    url(r'^unbook/(?P<machine_name>\w+)/(?P<booked_date>\d{8)/(P<booked_time>\d{2})/$', views.UnbookMachine, name='UnbookMachine'),
    url(r'^unbook/(?P<machine_name>\w+)/(?P<booked_date>\d{8})/(?P<booked_time>\w+)$', views.UnbookMachine, name='UnbookMachine'),
    url(r'^tomorrow/$',views.BookMachineTmr,name='BookMachineTmr'),

)
