
from django.conf.urls import patterns, include, url
from views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^$', index),
    ('^index/$', index),
    ('^phone_add/$', phone_add),
    ('^phones/$', phones),
    ('^phone_del/$', phone_del),
    ('^phone_settled/$', phone_settled),
    ('^phone_unsettled/$', phone_unsettled),
    ('^admin/$', admin),
    ('^setpwd/$', setpwd),
    ('^setadmin/$', setadmin),
    ('^user_del/$', user_del),

    ('^loginpage/$', loginpage),
    ('^registerpage/$', registerpage),
    ('^login/$', login),
    ('^logout/$', logout),
    ('^register/$', register),
)


# This will work if DEBUG is True
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
