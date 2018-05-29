from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.db.utils import IntegrityError
from users.models import CustomUser
from .forms import (
    MainForm, DirectoryForm, DirectoryItemForm
)
from .models import (
    Directory, DirectoryItem, ClassifiedByRelation, RootDirectory
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
        root_dir = RootDirectory.objects.using('directories').first()
        thumb_dir = RootDirectory.objects.using('directories').first().dir_100
    except ObjectDoesNotExist:
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
    return render(request, 'general-stat-log.html', locals())


@login_required(login_url='/accounts/login/')
def statistics_detail(request, pk):
    CustomUser.update_user_activity(user=request.user)
    current_user = get_object_or_404(CustomUser, pk=pk)
    dirs = ClassifiedByRelation.objects.using('directories').filter(user_id=current_user.id)
    return render(request, 'statistics_detail_log.html', locals())