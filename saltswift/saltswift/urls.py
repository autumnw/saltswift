from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'saltswift.views.home', name='home'),
    # url(r'^saltswift/', include('saltswift.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', 'default.views.index'),
    url(r'^cluster/$', 'default.views.cluster'),
    url(r'^monitor/$', 'default.views.monitor'),
    url(r'^server/$', 'default.views.index'),
    url(r'^server/(?P<host>.*)/$', 'server.views.serverdetails'),
)
