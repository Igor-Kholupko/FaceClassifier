from django.db import models


class RootDirectory(models.Model):
    path = models.CharField(max_length=256, unique=True)
    dir_100 = models.CharField(max_length=256)

    def __str__(self):
        return "%s" % self.path

    class Meta:
        verbose_name = "Root Directory"
        verbose_name_plural = "Root Directories"


class Directory(models.Model):
    root_dir = models.ForeignKey(RootDirectory, on_delete=models.CASCADE)
    path = models.CharField(max_length=256)
    is_busy = models.PositiveIntegerField(default=0)
    classifications_amount = models.PositiveIntegerField(default=0)
    directory_class = models.TextField(default="")

    def __str__(self):
        return "%s" % self.path

    class Meta:
        verbose_name = 'Directory'
        verbose_name_plural = 'Directories'


class ClassifiedByRelation(models.Model):
    dir = models.ForeignKey(Directory, on_delete=models.CASCADE)
    user_id = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Statistic record'
        verbose_name_plural = 'Statistic table'
        unique_together = ('dir', 'user_id')
        indexes = [
            models.Index(fields=['user_id']),
        ]


class DirectoryItem(models.Model):
    dir = models.ForeignKey(Directory, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    is_bad = models.BooleanField(default=False)
    # fullsize_image = models.ImageField(upload_to="", default=None)
    # thumbnail_100x100 = models.ImageField(upload_to="", default=None)
    # thumbnail_200x200 = models.ImageField(upload_to="", default=None)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Directory Item"
        verbose_name_plural = "Directory Items"
