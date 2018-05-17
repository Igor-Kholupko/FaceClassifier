import os


def populate_db(root_directory=None):
    from directories.models import Directory
    root_directory = os.listdir(root_directory)
    for i in root_directory:
        directory = Directory(path=i, is_classified=0)
        directory.save(using="directories")
