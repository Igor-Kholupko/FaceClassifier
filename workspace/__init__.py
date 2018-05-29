from django.contrib.auth.signals import (
    user_logged_in, user_logged_out
)
from django.dispatch import receiver
from regeneratedb import release_directories


@receiver(user_logged_in)
def _on_user_logged_in(sender, user, request, **kwargs):
    user.is_logged = True
    user.save()
    print("User \"%s\" logged in." % user.username)


@receiver(user_logged_out)
def _on_user_logged_out(sender, user, request, **kwargs):
    user.is_logged = False
    user.save()
    release_directories(user.id)
    print("User \"%s\" logged out." % user.username)
