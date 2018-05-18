from django.db import models


class RootDirectory(models.Model):
    path = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return "%s" % self.path

    class Meta:
        verbose_name = "Root Directory"
        verbose_name_plural = "Root Directories"


class Directory(models.Model):
    root_dir_id = models.IntegerField()
    path = models.CharField(max_length=256)
    is_classified = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.path

    class Meta:
        verbose_name = 'Directory'
        verbose_name_plural = 'Directories'


class DirectoryItem(models.Model):
    dir_id = models.IntegerField()
    name = models.CharField(max_length=256)
    is_bad = models.BooleanField()

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Directory Item"
        verbose_name_plural = "Directory Items"
