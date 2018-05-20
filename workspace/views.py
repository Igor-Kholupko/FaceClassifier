from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import (
    MainForm, DirectoryForm, DirectoryItemForm
)
from .models import (
    Directory, DirectoryItem,
)


@login_required(login_url='/accounts/login/')
def workspace(request):
    main_forms = MainForm
    if main_forms.dir_forms.__len__() == 0:
        for directory in Directory.objects.using('directories').filter(is_busy=False)[:10]:
            dir_form = DirectoryForm(data=directory)
            dir_form.item_forms = list()
            for item in DirectoryItem.objects.using('directories').filter(dir_id=directory):
                item_form = DirectoryItemForm(data=item)
                dir_form.item_forms.append(item_form)
            main_forms.dir_forms.append(dir_form)
    dictionary = dict()
    dictionary.update(main_forms=locals()['main_forms'])
    return render(request, 'Main.html', locals())
