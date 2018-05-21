from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import (
    MainForm, DirectoryForm, DirectoryItemForm
)
from .models import (
    Directory, DirectoryItem,
)
from threading import Lock
import re


# Lock for form synchronizing

lock = Lock()


# Max directories on page.

MAX_DIRECTORIES = 10


@login_required(login_url='/accounts/login/')
def workspace(request):
    if request.method == "POST":
        d = dict(request.POST)
        for i in range(1, MAX_DIRECTORIES):
            try:
                split = re.split("[_\s]", d[("radio_%d" % i)][0])
                i = Directory.objects.using('directories').get(pk=int(split[0]))
                i.classifications_amount += 1
                i.is_busy = '0'
                i.directory_class = split[1]
                i.save(using='directories')
            except KeyError:
                break
        try:
            checkboxes = d['checkbox']
            for i in checkboxes:
                i = DirectoryItem.objects.using('directories').get(id=i)
                i.is_bad = True
                i.save(using='directories')
        except KeyError:
            pass
    main_form = MainForm()
    if main_form.dir_forms.__len__() == 0 or request.method == "POST" or \
            (main_form.user_id.__len__() != 0 and main_form.user_id[-1] != request.user.id):
        lock.acquire()
        dir_list = list()
        if main_form.dir_forms.__len__() != 0 and request.method != "POST" and main_form.user_id[-1] != request.user.id:
            dir_list = Directory.objects.using('directories').filter(is_busy=request.user.id)
        main_form.dir_forms.clear()
        if dir_list.__len__() == 0:
            dir_list = Directory.objects.using('directories').filter(is_busy=0,
                                                                     classifications_amount=0)[:MAX_DIRECTORIES]
        for directory in dir_list:
            directory.is_busy = request.user.id
            directory.save(using='directories')
            dir_form = DirectoryForm(data=directory)
            dir_form.item_forms = list()
            for item in DirectoryItem.objects.using('directories').filter(dir_id=directory):
                item_form = DirectoryItemForm(data=item)
                dir_form.item_forms.append(item_form)
            main_form.dir_forms.append(dir_form)
        main_form.user_id.clear()
        main_form.user_id.append(request.user.id)
        lock.release()
    dictionary = dict()
    dictionary.update(main_form=locals()['main_form'])
    return render(request, 'Main.html', dictionary)
