import os
import sys
from django.db.utils import IntegrityError
from django.db.models import ObjectDoesNotExist


def populate_db(root_directory_path=None, thumb_directories=None, check=False, continue_fill=False):
    if check:
        sys.stdout.write("Start checking.\n")
        original_dir = os.path.normpath("D:/test/identities_0")
        thumbs_dir = os.path.normpath("D:/test/identities_0_100")
        original_dirs = os.listdir(original_dir)
        original_dirs.pop(original_dirs.index("zero_files.txt"))
        thumbs_dirs = os.listdir(thumbs_dir)
        original_dirs.sort()
        thumbs_dirs.sort()
        j = 0
        from workspace.models import Directory, StatisticDirectory
        for i in range(0, original_dirs.__len__()):
            if original_dirs[i] == thumbs_dirs[j]:
                if os.listdir(os.path.join(original_dir, original_dirs[i])).__len__() != os.listdir(os.path.join(thumbs_dir, thumbs_dirs[j])).__len__():
                    obj = Directory.objects.using("directories").get(path=original_dirs[i])
                    obj.directory_class = 'INVALID_FOLDER_CHECKED'
                    obj.classifications_amount = 1
                    if obj.id%10 == 0:
                        try:
                            obj2 = StatisticDirectory.objects.using("directories").get(dir_id=obj.id)
                            obj2.is_completed = True
                            obj2.save(using="directories")
                        except ObjectDoesNotExist:
                            pass
                    obj.save(using="directories")
                    sys.stdout.write(" - - [%d] : '%s' have missed thumbnails.\n" % (obj.id, obj.path))
                else:
                    sys.stdout.write("[%d] : '[unreaded path]' is god.\n" % i)
            else:
                obj = Directory.objects.using("directories").get(path=original_dirs[i])
                obj.directory_class = 'NO_THUMBNAILS'
                obj.classifications_amount = 1
                if obj.id%10 == 0:
                    try:
                        obj2 = StatisticDirectory.objects.using("directories").get(dir_id=obj.id)
                        obj2.is_completed = True
                        obj2.save(using="directories")
                    except ObjectDoesNotExist:
                        pass
                obj.save(using="directories")
                sys.stdout.write(" - - [%d] : '%s' doesn't have thumbnails folder.\n" % (obj.id, obj.path))
                continue
            j += 1
        sys.exit(0)
    if root_directory_path is None:
        sys.stdout.write("You must set ROOT_DIRECTORY variable in settings file.\n")
        sys.exit(0)
    from workspace.models import (
        Directory, RootDirectory, DirectoryItem, StatisticDirectory
    )
    root_directory = RootDirectory(path=root_directory_path, dir_full=thumb_directories[0], dir_100=thumb_directories[1])
    try:
        root_directory.save(using="directories")
    except IntegrityError:
        sys.stdout.write("Root \"%s\" already imported." % root_directory_path)
        if not continue_fill:
            sys.stdout.write("\n")
            sys.exit(1)
        root_directory = RootDirectory.objects.using("directories").get(path=root_directory_path)
        sys.stdout.write(" Check for non-imported directories.\n\n")
    try:
        root_directory_content = os.listdir(root_directory.path)
    except FileNotFoundError:
        RootDirectory.objects.using("directories").last().delete()
        sys.stdout.write("Root \"%s\" cannot be found.\n" % root_directory_path)
        sys.exit(1)
    sys.stdout.write("Start importing from \"%s\".\n\n" % root_directory_path)
    dirs_amount = root_directory_content.__len__()
    global counter
    thumbnails_full_path = os.path.join(os.path.dirname(root_directory_path), thumb_directories[1])
    for counter, i in enumerate(root_directory_content):
        directory = Directory(root_dir=root_directory, path=i)
        try:
            directory.save(using="directories")
            directory_content = os.listdir(os.path.join(root_directory.path, directory.path))
            global photos_counter
            for photos_counter, j in enumerate(directory_content):
                directory_item = DirectoryItem(dir=directory, name=j, is_bad=False)
                directory_item.save(using="directories")
            try:
                if os.listdir(os.path.join(thumbnails_full_path, directory.path)).__len__() == 0:
                    directory.classifications_amount = 1
                    directory.directory_class = "TrashFolder"
                    directory.save(using="directories")
                    sys.stdout.write(" - - [%d] : '%s' was empty.\n" % (counter+1, i))
                else:
                    sys.stdout.write("[%d] : '%s' imported (%d photos).\n" % (counter+1, i, photos_counter+1))
                if (counter+1) % 10 == 0:
                    directory_clone = StatisticDirectory(dir=directory)
                    if os.listdir(os.path.join(thumbnails_full_path, directory.path)).__len__() == 0:
                        directory_clone.is_completed = True
                    directory_clone.save(using='directories')
            except FileNotFoundError:
                    directory.classifications_amount = 1
                    directory.directory_class = "TrashFolder"
                    directory.save(using="directories")
                    sys.stdout.write(" - - [%d] : '%s' thumbnails folder missed.\n" % (counter+1, i))
        except IntegrityError:
            dirs_amount -= 1
            continue
    if dirs_amount == 0:
        sys.stdout.write("All directories has been imported earlier.\n")
    elif dirs_amount == root_directory_content.__len__():
        sys.stdout.write("\nDirectories (%d) from root \"%s\" are imported.\n" % (counter+1, root_directory_path))
    else:
        sys.stdout.write("\nAdded %d directories from root \"%s\".\n" % (dirs_amount, root_directory_path))
