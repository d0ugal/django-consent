from django.dispatch import Signal

pre_consent_granted = Signal(providing_args=["consent", ])
post_consent_granted = Signal(providing_args=["consent", ])

pre_consent_revoked = Signal(providing_args=["consent", ])
post_consent_revoked = Signal(providing_args=["consent", ])
