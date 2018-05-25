from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    number_of_sorted_folders = models.PositiveSmallIntegerField(default=0)
    last_activity = models.DateTimeField(default=timezone.now)
    quality_of_work = models.DecimalField(default=0.0, max_digits=5, decimal_places=4)
    number_of_sorted_folders_at_a_time = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.username

    @staticmethod
    def update_user_activity(user):
        """Updates the timestamp a user has for their last action. Uses UTC time."""
        CustomUser.objects.update_or_create(id=user.id, defaults={'last_activity': timezone.now()})

    @staticmethod
    def get_user_activities(time_delta=timedelta(minutes=10)):
        starting_time = timezone.now() - time_delta
        return CustomUser.objects.filter(last_activity__gte=starting_time).order_by('-last_activity')