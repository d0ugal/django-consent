from django.conf.urls.defaults import patterns, url, include

from consent.views import PrivilegeListView, ConsentEditView

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^$', PrivilegeListView.as_view(), name="privileges"),
    url(r'^edit/$', ConsentEditView.as_view(), name="edit_privileges"),

)
