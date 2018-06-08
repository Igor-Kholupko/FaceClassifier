from django.contrib.auth.signals import (
    user_logged_in, user_logged_out
)
from django.dispatch import receiver
from regeneratedb import release_directories
from journal import log_message


@receiver(user_logged_in)
def _on_user_logged_in(sender, user, request, **kwargs):
    try:
        user.is_logged = True
        user.save()
        log_message("User \"%s\" logged in." % user.username)
    except AttributeError:
        pass


@receiver(user_logged_out)
def _on_user_logged_out(sender, user, request, **kwargs):
    try:
        user.is_logged = False
        user.save()
        release_directories(user.id)
        log_message("User \"%s\" logged out." % user.username)
    except AttributeError:
        pass
