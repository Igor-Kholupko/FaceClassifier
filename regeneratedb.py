from django.core.exceptions import AppRegistryNotReady
from django.conf import settings
from time import sleep
from journal import log_message


def release_directories(user_id=0):
    if user_id > 0:
        try:
            from workspace.models import Directory
            dirs_list = Directory.objects.using('directories').filter(is_busy=user_id)
            for directory in dirs_list:
                directory.is_busy = 0
                directory.save(using='directories')
        except ModuleNotFoundError or AppRegistryNotReady:
            pass


def regeneration_thread():
    while True:
        sleep(settings.REGENERATION_TIMER)
        try:
            from users.models import CustomUser
            for user in CustomUser.objects.filter(is_logged=True):
                if not user.is_online():
                    release_directories(user.id)
        except ModuleNotFoundError or AppRegistryNotReady:
            continue
        log_message("DATABASE REGENERATION")
