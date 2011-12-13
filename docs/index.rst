Django Consent
========================================

A Django app for managing permissions that a user has granted the website to
do. This could be used for a number of requests, from asking the user if you
can post to their twitter, or send them newsletter updates.

The app has no requirements, but supports south for migrations and is tested
to work on Django 1.3 and Django trunk. It is tested on Python 2.6.

Contents
========

.. toctree::
 :maxdepth: 1

 models
 views
 changelog

Installation
========================================

Use pip::

    pip install django-appregister

Or, if you must::

    easy_install django-appregister

After installing, add 'consent' to your ``INSTALLED_APPS`` and run a syncdb or
a migrate if you are using south.

You will then need to integrate the views into your urls.py.

.. doctest::

    from consent.views import ConsentListView, ConsentEditView

    urlpatterns = patterns('',
        url(r'^$', ConsentListView.as_view(), name="privileges"),
        url(r'^edit/$', ConsentEditView.as_view(), name="edit_privileges"),
    )