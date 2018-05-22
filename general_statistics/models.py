from django.contrib.auth.models import User
import datetime
from django.conf import settings


class Profile(User):
    class Meta:
        proxy = True


def online(self):
    if self.last_seen():
        now = datetime.datetime.now()
        print(now)
        if now > self.last_seen() + datetime.timedelta(
                     seconds=settings.USER_ONLINE_TIMEOUT):
            print(self.last_seen() + datetime.timedelta(
                     seconds=settings.USER_ONLINE_TIMEOUT))
            return False
        else:
            return True
    else:
        return False

