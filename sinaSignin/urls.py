from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from sina.views import sinaindex
from sina.views import rsaLogin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sinaSignin.views.home', name='home'),
    # url(r'^sinaSignin/', include('sinaSignin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', rsaLogin),
    url(r'^weiboindex/$', sinaindex),
)
