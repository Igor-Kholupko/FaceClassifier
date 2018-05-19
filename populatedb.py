import os
import sys
from django.db.utils import IntegrityError


def populate_db(root_directory=None):
    if root_directory is None:
        sys.stdout.write("You must set ROOT_DIRECTORY variable in settings file.\n")
        sys.exit(0)
    from directories.models import (
        Directory, RootDirectory, DirectoryItem,
    )
    root_directory = RootDirectory(path=os.path.normpath(root_directory))
    try:
        root_directory.save(using="directories")
    except IntegrityError:
        sys.stdout.write("Root path is already imported.\n")
        sys.exit(1)
    try:
        root_directory_content = os.listdir(root_directory.path)
    except FileNotFoundError:
        RootDirectory.objects.using("directories").last().delete()
        sys.stdout.write("Root path cannot be found.\n")
        sys.exit(1)
    for i in root_directory_content:
        directory = Directory(root_dir=root_directory, path=i, is_classified=0)
        directory.save(using="directories")
        directory_content = os.listdir(root_directory.path + "\\" + directory.path)
        for j in directory_content:
            directory_item = DirectoryItem(dir=directory, name=j, is_bad=False,
                                           thumbnail_100x100=directory.path + "\\" + j,
                                           thumbnail_200x200=directory.path + "\\" + j)
            directory_item.save(using="directories")
