from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

app_name = 'hackerspace'

urlpatterns = [
    # Examples:
    # url(r'^$', 'hackerspace.views.home', name='home'),
    # url(r'^hackerspace/', include('hackerspace.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    url(r'^', include('members.urls', namespace="members")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
