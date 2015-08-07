from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
	#for workout summaries
	url(r'^$', views.workoutsummary, name='workoutsummary'),
	url(r'^(?P<page_id>\d+)/$', views.workoutsummary, name='workoutsummary'),
	#for personal work out chart summaries
	url(r'^requestpersonalchart/$', views.personalworkoutchart, name='requestpersonalworkoutchart'),
	#for community stats summaries
	url(r'^community/$', views.communityStats, name='communityStats'),
)
