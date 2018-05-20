from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import MainForm
from .models import (
    Directory, DirectoryItem,
)


@login_required(login_url='/accounts/login/')
def workspace(request):
    main_forms = MainForm
    for i in Directory.objects.using('directories').filter(is_busy=False)[0:19]:
        items = DirectoryItem.objects.using('directories').filter(dir_id=i)
        id_list = list()
        for j in items:
            id_list.append((j.pk, j.name))
        main_forms.list_of_tuples.append((i.id, i.path, id_list))
    return render(request, 'Main.html', locals())
