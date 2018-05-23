from django.core.exceptions import AppRegistryNotReady
from django.conf import settings
from time import sleep
# from [user_model_module] import [user_class]


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
        """
        for user in [user_class].objects.all():
            if not user.is_online:
                release_directories(user.id)
        """
        print("DATABASE REGENERATION")
