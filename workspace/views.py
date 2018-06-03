from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.db.utils import IntegrityError
from users.models import CustomUser
from .forms import (
    MainForm, DirectoryForm, DirectoryItemForm
)
from .models import (
    Directory, DirectoryItem, ClassifiedByRelation, RootDirectory, StatisticDirectory
)
from threading import Lock
from _thread import start_new_thread
from regeneratedb import regeneration_thread
import re


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
        d = dict(request.POST)
        for i in range(1, MAX_DIRECTORIES+1):
            try:
                split = re.split("[_\s]", d[("radio_%d" % i)][0])
                i = Directory.objects.using('directories').get(pk=int(split[0]))
                i.classifications_amount += 1
                i.is_busy = 0
                i.directory_class = split[1]
                i.save(using='directories')
                classified_by = ClassifiedByRelation(dir=i, user_id=request.user.id)
                if i.classifications_amount == 3:
                    stat_dir = StatisticDirectory.objects.using('directories').get(pk=int(split[0]))
                    first_user = CustomUser.objects.get(pk=int(classified_by))
                    second_user = CustomUser.objects.get(pk=int(stat_dir.user_id_one))
                    third_user = CustomUser.objects.get(pk=int(stat_dir.user_id_two))
                    if i.directory_class == stat_dir.directory_class_one:
                        if stat_dir.directory_class_one == stat_dir.directory_class_two:
                            first_user.quality_of_work = (first_user.quality_of_work + 1)/2
                            second_user.quality_of_work = (second_user.quality_of_work + 1)/2
                            third_user.quality_of_work = (third_user.quality_of_work + 1)/2
                        else:
                            first_user.quality_of_work = (first_user.quality_of_work + 1) / 2
                            second_user.quality_of_work = (second_user.quality_of_work + 1) / 2
                            third_user.quality_of_work /= 2
                    else:
                        if i.directory_class == stat_dir.directory_class_two:
                            first_user.quality_of_work = (first_user.quality_of_work + 1) / 2
                            second_user.quality_of_work /= 2
                            third_user.quality_of_work = (third_user.quality_of_work + 1) / 2
                        else :
                            if stat_dir.directory_class_one == stat_dir.directory_class_two:
                                first_user.quality_of_work /= 2
                                second_user.quality_of_work = (second_user.quality_of_work + 1) / 2
                                third_user.quality_of_work = (third_user.quality_of_work + 1) / 2
                            else:
                                first_user.quality_of_work = 0
                                second_user.quality_of_work = 0
                                third_user.quality_of_work = 0
                    first_user.save()
                    second_user.save()
                    third_user.save()
                try:
                    classified_by.save(using='directories')
                except IntegrityError:
                    pass
            except KeyError:
                continue
        CustomUser.update_user_number_of_sorted_folders(request.user)
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
    dir_list = QuerySet()
    dir_list = Directory.objects.using('directories').filter(is_busy=request.user.id)
    if dir_list.__len__() < MAX_DIRECTORIES:
        dir_list = (dir_list | (Directory.objects.using('directories').filter(is_busy=0, classifications_amount=0)))[:MAX_DIRECTORIES]
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
    dictionary = dict(main_form=locals()['main_form'], root_dir=locals()['root_dir'], thumb_dir=locals()['thumb_dir'])
    ret_val = render(request, 'main.html', dictionary)
    lock.release()
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
