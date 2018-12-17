import os.path
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from members import views
site_media = os.path.join(os.path.dirname(__file__), 'site_media')

app_name = 'members'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^reset/$', views.reset_page, name='reset'),
    url(r'^reset/(?P<reset_code>.+)/$', views.reset_code, name='reset_code'),
    url(r'^logout/$', views.logout_page, name='logout'),
    url(r'^register/$', views.register_page, name='register'),
    url(r'^member_info/$', views.member_info, name='member_info'),
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^classes/$', views.classes, name='classes'),
    url(r'^blog/$', views.blog, name='blog'),
    url(r'^register/success/$', views.register_success,name='success'),
    #url(r'^member/$', views.member,name='member'),
    url(r'^payment/$', views.payment,name='payment'),
    url(r'^payment/methods/$', views.payment_methods,name='payment_methods'),
    url(r'^payment/history/$', views.payment_history,name='payment_history'),
    url(r'^subscriptions/$', views.subscriptions,name='subscriptions'),
    url(r'^pr_request/$', views.pr_request,name='pr_request'),
    url(r'^events/$', views.events,name='events'),
    url(r'^contact_us/$', views.contact_us,name='contact_us'),
    url(r'^terms/$', views.terms,name='terms'),
    url(r'^faq/$', views.faq,name='faq'),
    url(r'^faqs/$', views.faq,name='faq'),
    url(r'^user_groups/$', views.user_groups,name='user_groups'),

    #{ 'template': 'registration/register_success.html' }),
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    #{ 'document_root': site_media }),
   # url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
   # url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
   # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
]
