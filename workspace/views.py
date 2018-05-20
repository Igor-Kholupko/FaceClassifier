from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import MainForm
from .models import (
    Directory, DirectoryItem,
)


@login_required(login_url='/accounts/login/')
def workspace(request):
    main_form = MainForm
    for i in Directory.objects.using('directories').filter(is_busy=False)[0:19]:
        items = DirectoryItem.objects.using('directories').filter(dir_id=i)
        id_list = list()
        for j in items:
            id_list.append((j.pk, j.thumbnail_100x100, j.thumbnail_200x200))
        main_form.list_of_tuples.append((i.id, id_list))
    return render(request, 'Main.html', locals())
