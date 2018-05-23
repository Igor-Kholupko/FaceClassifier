from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    number_of_sorted_folders = models.PositiveSmallIntegerField(default=0)
    last_activity = models.DateTimeField()
    quality_of_work = models.DecimalField(default=0.0, max_digits=5, decimal_places=4)
    number_of_sorted_folders_at_a_time = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.user.username

    def is_online(self):
        time_delta = timedelta(minutes=10)
        starting_time = timezone.now() - time_delta
        if self.last_activity < starting_time:
            return False
        else:
            return True

    @staticmethod
    def update_user_activity(user):
        """Updates the timestamp a user has for their last action. Uses UTC time."""
        Profile.objects.update_or_create(update=user, defaults={'last_activity': timezone.now()})

    @staticmethod
    def get_user_activities(time_delta=timedelta(minutes=10)):
        starting_time = timezone.now() - time_delta
        return Profile.objects.filter(last_activity__gte=starting_time).order_by('-last_activity')
