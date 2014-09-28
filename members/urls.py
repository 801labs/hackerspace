import os.path
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from members import views
site_media = os.path.join(os.path.dirname(__file__), 'site_media')

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout_page, name='logout'),
    url(r'^register/$', views.register_page, name='register'),
    url(r'^member_info/$', views.member_info, name='member_info'),
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^register/success/$', views.register_success,name='success'),
    #url(r'^member/$', views.member,name='member'),
    url(r'^payment/$', views.payment,name='payment'),
    url(r'^subscriptions/$', views.subscriptions,name='subscriptions')

    #{ 'template': 'registration/register_success.html' }),
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    #{ 'document_root': site_media }),
   # url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
   # url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
   # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)
