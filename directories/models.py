from django.db import models


class Directory(models.Model):
    path = models.CharField(max_length=256)
    is_classified = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.path

    class Meta:
        verbose_name = 'Directory'
        verbose_name_plural = 'Directories'
