Django Consent
========================================

A Django app for managing permissions that a user has granted the website to do.
This could be used for a number of requests, from asking the user if you can
post to their twitter, or send them newsletter updates.

The app has no requirements, but supports south for migrations and is tested to
work on Django 1.3 and Django trunk. It is tested on Python 2.6.


Installation
========================================

Use pip::

    pip install django-appregister

Or, if you must::

    easy_install django-appregister


Model Reference
========================================

.. automodule:: consent.models

.. autoclass:: Privilege

    .. attribute:: name

        ``CharField(max_length=64)``
        The name of the Privilege

    .. attribute:: description

        ``TextField()``
        A user friendly description to state what granting the privilege would
        mean.

    .. attribute:: users

        ``ManyToManyField(User, through='consent.Consent')``
        The users that have granted and revoked this Privilege.

        .. note::

            This will have **all** users that have interacted with the consent
            by granting or then revoking the privilege. It will not show users
            that have never granted it.


.. autoclass:: Consent

    .. attribute:: user

        ``ForeignKey(User)``

    .. attribute:: privilege

        ``ForeignKey(Privilege)``

    .. attribute:: granted_on

        ``models.DateTimeField(default=datetime.now)``
        When the Privilege was originally granted by the user.

    .. attribute:: revoked_on

        ``models.DateTimeField(null=True, blank=True)``
        When the Privilege was revoked by the user. If it has never been
        revoked this will be ``None``

    .. attribute:: revoked

        ``models.BooleanField(default=False)``
        A Boolean field designating if the Privilege has been revoked or not.

        .. note::

            By default it is assumed when a ``Consent`` instance is being
            created a user is granting it. If a ``Consent`` does not exist for
            that User and Privilege then it has never been granted.

    .. automethod:: revoke
    .. automethod:: grant

.. autoclass:: ConsentManager


Views Reference
========================================

.. automodule:: consent.views

.. autoclass:: PrivilegeListView
    :members:

.. autoclass:: PrivilegeEditView
    :members: