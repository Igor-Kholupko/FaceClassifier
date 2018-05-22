from django.contrib.auth.signals import (
    user_logged_in, user_logged_out
)
from django.dispatch import receiver


@receiver(user_logged_in)
def _on_user_logged_in(sender, user, request, **kwargs):
    print("User: %d logged in." % user.id)


@receiver(user_logged_out)
def _on_user_logged_out(sender, user, request, **kwargs):
    print("User: %d logged out." % user.id)
