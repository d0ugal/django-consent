from django.conf.urls.defaults import patterns, url, include

from consent.views import ConsentListView, ConsentEditView

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^$', ConsentListView.as_view(), name="privileges"),
    url(r'^edit/$', ConsentEditView.as_view(), name="edit_privileges"),

)
