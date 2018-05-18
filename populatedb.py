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
    root_directory_id = root_directory.id
    root_directory_path = root_directory.path
    try:
        root_directory = os.listdir(root_directory.path)
    except FileNotFoundError:
        RootDirectory.objects.using("directories").last().delete()
        sys.stdout.write("Root path cannot be found.\n")
        sys.exit(1)
    for i in root_directory:
        directory = Directory(root_dir_id=root_directory_id, path=i, is_classified=0)
        directory.save(using="directories")
        directory_id = directory.id
        directory = os.listdir(root_directory_path + "\\" + directory.path)
        for j in directory:
            directory_item = DirectoryItem(dir_id=directory_id, name=j, is_bad=False)
            directory_item.save(using="directories")
