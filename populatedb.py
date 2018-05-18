import os
import sys
from django.db.utils import IntegrityError


def populate_db(root_directory=None):
    from directories.models import (
        Directory, RootDirectory, DirectoryItem,
    )
    root_directory = RootDirectory(path=root_directory)
    try:
        root_directory.save(using="directories")
    except IntegrityError:
        sys.stdout.write("Root path is already imported.\n")
        sys.exit(1)
    root_directory = os.listdir(root_directory.path)
    for i in root_directory:
        directory = Directory(path=i, is_classified=0)
        directory.save(using="directories")
