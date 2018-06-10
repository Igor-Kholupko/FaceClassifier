from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.utils import timezone
from users.models import CustomUser
from .forms import (
    MainForm, DirectoryForm, DirectoryItemForm
)
from .models import (
    Directory, DirectoryItem, ClassifiedByRelation, RootDirectory, StatisticDirectory
)
import journal
from threading import Lock
from _thread import start_new_thread
from regeneratedb import regeneration_thread
import re
from decimal import Decimal


# Lock for form synchronizing

lock = Lock()


# Starting regeneration thread

start_new_thread(regeneration_thread, ())


# Max directories on page.

MAX_DIRECTORIES = 10


@login_required(login_url='/accounts/login/')
def workspace(request):
    lock.acquire()
    CustomUser.update_user_activity(request.user)
    try:
        root_dir = RootDirectory.objects.using('directories').first().dir_full
        thumb_dir = RootDirectory.objects.using('directories').first().dir_100
    except (ObjectDoesNotExist, AttributeError):
        root_dir = None
        thumb_dir = None
        pass
    main_form = MainForm()
    if request.method == "POST":
        time_moment = timezone.timedelta(hours=timezone.now().time().hour, minutes=timezone.now().time().minute, seconds=timezone.now().second)
        d = dict(request.POST)
        dirs_counter = 0
        for i in range(1, MAX_DIRECTORIES+1):
            try:
                split = re.split("[_\s]", d[("radio_%d" % i)][0])
                i = Directory.objects.using('directories').get(pk=int(split[0]))
                dirs_counter += 1
                i.classifications_amount += 1
                if i.classifications_amount == 1:
                    i.is_busy = 0
                    i.directory_class = split[1]
                    i.save(using='directories')
                    classified_by = ClassifiedByRelation(dir=i, user_id=request.user.id)
                    try:
                        classified_by.save(using='directories')
                    except IntegrityError:
                        pass
                elif i.classifications_amount == 2:
                    stat_info = StatisticDirectory.objects.using('directories').get(dir=i)
                    stat_info.user_id_one = request.user.id
                    request.user.number_of_checked_folders += 1
                    request.user.save()
                    stat_info.directory_class_one = split[1]
                    i.is_busy = 0

                    i.save(using='directories')
                    try:
                        stat_info.save(using='directories')
                    except IntegrityError:
                        pass
                else:
                    stat_info = StatisticDirectory.objects.using('directories').get(dir=i)
                    stat_info.user_id_two = request.user.id
                    stat_info.directory_class_two = split[1]
                    stat_info.is_completed = True
                    i.is_busy = 0
                    i.save(using='directories')
                    try:
                        stat_info.save(using='directories')
                    except IntegrityError:
                        pass
                    classified_by_one = ClassifiedByRelation.objects.using('directories').get(dir=i)
                    stat_dir = StatisticDirectory.objects.using('directories').get(dir_id=int(split[0]))
                    first_user = CustomUser.objects.get(pk=int(classified_by_one.user_id))
                    second_user = CustomUser.objects.get(pk=int(stat_dir.user_id_one))
                    third_user = CustomUser.objects.get(pk=int(stat_dir.user_id_two))
                    if i.directory_class == stat_dir.directory_class_one:
                        if stat_dir.directory_class_one == stat_dir.directory_class_two:
                            a = (first_user.quality_of_work*first_user.number_of_sorted_folders/Decimal("9")+1)/(first_user.number_of_sorted_folders/Decimal("9")+1)
                            first_user.quality_of_work = (first_user.quality_of_work*first_user.number_of_sorted_folders/Decimal("9")+1)/(first_user.number_of_sorted_folders/Decimal("9")+1)
                            second_user.quality_of_work = (second_user.quality_of_work*second_user.number_of_sorted_folders/Decimal("9")+1)/(second_user.number_of_sorted_folders/Decimal("9")+1)
                            third_user.quality_of_work = (third_user.quality_of_work*third_user.number_of_sorted_folders/Decimal("9")+1)/(third_user.number_of_sorted_folders/Decimal("9")+1)
                        else:
                            first_user.quality_of_work = (first_user.quality_of_work*first_user.number_of_sorted_folders/Decimal("9")+1)/(first_user.number_of_sorted_folders/Decimal("9")+1)
                            second_user.quality_of_work = (second_user.quality_of_work*second_user.number_of_sorted_folders/Decimal("9")+1)/(second_user.number_of_sorted_folders/Decimal("9")+1)
                            third_user.quality_of_work = (third_user.quality_of_work*third_user.number_of_sorted_folders/Decimal("9"))/(third_user.number_of_sorted_folders/Decimal("9")+1)
                    elif i.directory_class == stat_dir.directory_class_two:
                        first_user.quality_of_work = (first_user.quality_of_work*first_user.number_of_sorted_folders/Decimal("9")+1)/(first_user.number_of_sorted_folders/Decimal("9")+1)
                        second_user.quality_of_work = (second_user.quality_of_work*second_user.number_of_sorted_folders/Decimal("9"))/(second_user.number_of_sorted_folders/Decimal("9")+1)
                        third_user.quality_of_work = (third_user.quality_of_work*third_user.number_of_sorted_folders/Decimal("9")+1)/(third_user.number_of_sorted_folders/Decimal("9")+1)
                    elif stat_dir.directory_class_one == stat_dir.directory_class_two:
                        first_user.quality_of_work = (first_user.quality_of_work*first_user.number_of_sorted_folders/Decimal("9"))/(first_user.number_of_sorted_folders/Decimal("9")+1)
                        second_user.quality_of_work = (second_user.quality_of_work*second_user.number_of_sorted_folders/Decimal("9")+1)/(second_user.number_of_sorted_folders/Decimal("9")+1)
                        third_user.quality_of_work = (third_user.quality_of_work*third_user.number_of_sorted_folders/Decimal("9")+1)/(third_user.number_of_sorted_folders/Decimal("9")+1)
                        prev_class = i.directory_class
                        i.directory_class = stat_dir.directory_class_one
                        stat_dir.directory_class_one = prev_class
                        classified_by_one.user_id = second_user.id
                        stat_dir.user_id_one = first_user.id
                        i.save(using='directories')
                        stat_dir.save(using='directories')
                        classified_by_one.save(using='directories')
                    else:
                        first_user.quality_of_work = (first_user.quality_of_work*first_user.number_of_sorted_folders/Decimal("9"))/(first_user.number_of_sorted_folders/Decimal("9")+1)
                        second_user.quality_of_work = (second_user.quality_of_work*second_user.number_of_sorted_folders/Decimal("9"))/(second_user.number_of_sorted_folders/Decimal("9")+1)
                        third_user.quality_of_work = (third_user.quality_of_work*third_user.number_of_sorted_folders/Decimal("9"))/(third_user.number_of_sorted_folders/Decimal("9")+1)
                        journal.log_message("Dir %s(%d) differently classified by '%s', '%s', '%s'!\n" % (i.path, stat_dir.dir_id, first_user.username, second_user.username, third_user.username))
                        journal.log_to_file("bad-folders.log", "Dir %s(%d) differently classified by '%s', '%s', '%s'!\n" % (i.path, stat_dir.dir_id, first_user.username, second_user.username, third_user.username))
                    try:
                        first_user.number_of_checked_folders += 1
                        first_user.save()
                        second_user.save()
                        third_user.save()
                    except IntegrityError:
                        pass
            except KeyError:
                continue
        CustomUser.update_user_number_of_sorted_folders(request.user)
        user = CustomUser.objects.get(id=request.user.id)
        if user.average_folder_time == 0:
            user.average_folder_time = (time_moment - user.last_main_get_request)/dirs_counter
        else:
            user.average_folder_time = ((time_moment - timezone.timedelta(hours=user.last_main_get_request.hour,
                                                                         minutes=user.last_main_get_request.minute,
                                                                         seconds=user.last_main_get_request.second))/dirs_counter + user.average_folder_time)/2
        user.save()
        try:
            checkboxes = d['checkbox']
            for i in checkboxes:
                i = DirectoryItem.objects.using('directories').get(id=i)
                i.is_bad = True
                i.save(using='directories')
        except KeyError:
            pass
        lock.release()
        return redirect('/workspace/')
    dir_list = Directory.objects.using('directories').filter(is_busy=request.user.id)
    shared_folder = Directory.objects.none()
    if dir_list.exclude(classifications_amount=0).__len__() == 0:
        shared_folder_id = StatisticDirectory.objects.using('directories').filter(is_completed=False).exclude(user_id_one=request.user.id).exclude(user_id_two=request.user.id)
        for j in shared_folder_id:
            try:
                tmp = ClassifiedByRelation.objects.using('directories').get(dir_id=j.dir_id)
            except ObjectDoesNotExist:
                shared_folder = Directory.objects.using('directories').filter(is_busy=0, id=j.dir_id)
                if shared_folder.__len__() == 0:
                    continue
                break
            if tmp.user_id != request.user.id:
                shared_folder = Directory.objects.using('directories').filter(is_busy=0, id=j.dir_id)
                if shared_folder.__len__() == 0:
                    continue
                break
    dir_list = (dir_list | shared_folder | (Directory.objects.using('directories').filter(is_busy=0, classifications_amount=0)))[:MAX_DIRECTORIES]
    if dir_list.__len__() == shared_folder.__len__():
        dir_list = Directory.objects.none()
    dir_forms = list()
    dir_forms.clear()
    for directory in dir_list:
        directory.is_busy = request.user.id
        directory.save(using='directories')
        dir_form = DirectoryForm(data=directory)
        dir_form.item_forms = list()
        for item in DirectoryItem.objects.using('directories').filter(dir_id=directory):
            item_form = DirectoryItemForm(data=item)
            dir_form.item_forms.append(item_form)
        dir_forms.append(dir_form)
    main_form.dir_forms = dir_forms.copy()
    main_form.user_id.clear()
    main_form.user_id.append(request.user.id)
    dictionary = {'main_form': main_form, 'root_dir': root_dir, 'thumb_dir': thumb_dir}
    # dictionary = dict(main_form=locals()['main_form'], root_dir=locals()['root_dir'], thumb_dir=locals()['thumb_dir'])
    ret_val = render(request, 'main.html', dictionary)
    lock.release()
    CustomUser.update_last_main_get_request(request.user)
    return ret_val


@login_required(login_url='/accounts/login/')
def statistics(request):
    CustomUser.update_user_activity(user=request.user)
    current_user = request.user
    dirs = ClassifiedByRelation.objects.using('directories').filter(user_id=request.user.id)
    return render(request, 'user-stat.html', locals())


@login_required(login_url='/accounts/login/')
def general_statistics(request):
    CustomUser.update_user_activity(user=request.user)
    users = CustomUser.objects.all()
    dirs_all = Directory.objects.using('directories').count()
    dirs_classified = Directory.objects.using('directories').exclude(classifications_amount=0).count()
    percent = dirs_classified/dirs_all*100
    return render(request, 'general-stat-log.html', locals())


@login_required(login_url='/accounts/login/')
def statistics_detail(request, pk):
    CustomUser.update_user_activity(user=request.user)
    current_user = get_object_or_404(CustomUser, pk=pk)
    dirs = ClassifiedByRelation.objects.using('directories').filter(user_id=current_user.id)
    return render(request, 'statistics_detail_log.html', locals())


@login_required(login_url='/accounts/login/')
def password_edit(request):
    u = CustomUser.objects.get(username=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was updated successfully!')
            return redirect('password_edit')
        else:
            messages.warning(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_edit.html', {'form': form})


@login_required(login_url='/accounts/login/')
def help(request):
    return render(request, 'help.html')


def service_stopped(request):
    return render(request, 'service-stopped.html')
