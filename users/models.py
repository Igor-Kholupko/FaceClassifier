from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils import timezone
from workspace.models import ClassifiedByRelation


class CustomUser(AbstractUser):
    is_logged = models.BooleanField(default=False)
    number_of_sorted_folders = models.PositiveSmallIntegerField(default=0)
    number_of_checked_folders = models.PositiveSmallIntegerField(default=0)
    last_activity = models.DateTimeField(default=timezone.now)
    quality_of_work = models.DecimalField(default=1.0, max_digits=5, decimal_places=4)
    number_of_sorted_folders_at_a_time = models.PositiveSmallIntegerField(default=0)
    last_main_get_request = models.TimeField(default=timezone.datetime(year=1980, month=1, day=1, hour=0, minute=0, second=0))
    average_folder_time = models.DurationField(default=timezone.timedelta(microseconds=0))

    def __str__(self):
        return self.username

    def is_online(self):
        if not self.is_logged:
            return False
        else:
            starting_time = timezone.now() - settings.USER_INACTIVITY_TIME
            if self.last_activity > starting_time:
                return True
            else:
                return False

    @staticmethod
    def update_user_number_of_sorted_folders(user):
        num = ClassifiedByRelation.objects.using('directories').filter(user_id=user.id).__len__()
        CustomUser.objects.update_or_create(id=user.id,
                                            defaults={'number_of_sorted_folders': num})

    @staticmethod
    def update_last_main_get_request(user):
        CustomUser.objects.update_or_create(id=user.id, defaults={'last_main_get_request': timezone.now().time()})

    @staticmethod
    def update_user_activity(user):
        """Updates the timestamp a user has for their last action. Uses UTC time."""
        CustomUser.objects.update_or_create(id=user.id, defaults={'last_activity': timezone.now()})

    @staticmethod
    def get_user_activities(time_delta=settings.USER_INACTIVITY_TIME):
        starting_time = timezone.now() - time_delta
        return CustomUser.objects.filter(last_activity__gte=starting_time).order_by('-last_activity')
