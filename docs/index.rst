Django Consent
========================================

A Django app for managing privileges that a user has granted the website.
These differ from permissions where the website defines what a user can do,
but rather are what the user gives the website permission to do. This could be
used for example when asking the user if you can post to their twitter, or
send them newsletter updates.

This app has no external requirements beyond Django 1.3+ and is tested and
developed for Python 2.6+

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

You will then need to integrate the views into your urls.py. This adds a view
for the user see see all the privileges and also to edit them.

.. doctest::

    from consent.views import ConsentListView, ConsentEditView

    urlpatterns = patterns('',
        url(r'^$', ConsentListView.as_view(), name="privileges"),
        url(r'^edit/$', ConsentEditView.as_view(), name="edit_privileges"),
    )