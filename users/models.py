from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    number_of_sorted_folders = models.PositiveSmallIntegerField(default=0)
    time_of_work = models.DurationField
    quality_of_work = models.DecimalField(default=0.0, max_digits=5, decimal_places=4)
    number_of_sorted_folders_at_a_time = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.username
