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
    main_form = MainForm()
    cur_user = request.user
    if cur_user.id != main_form.user_id:
        main_form.user_id = cur_user.id
        main_form.dir_forms = list()
    if main_form.dir_forms.__len__() == 0:
        for directory in Directory.objects.using('directories').filter(is_busy='0')[:10]:
            #if directory.is_busy == '0':
            #    directory.is_busy = ("%d" % cur_user.id)
            #else:
            #    directory.is_busy += (",%d" % cur_user.id)
            #directory.save(using='directories')
            dir_form = DirectoryForm(data=directory)
            dir_form.item_forms = list()
            for item in DirectoryItem.objects.using('directories').filter(dir_id=directory):
                item_form = DirectoryItemForm(data=item)
                dir_form.item_forms.append(item_form)
            main_form.dir_forms.append(dir_form)
    if request.method == "POST":
        #main_form.data = main_form.cleaned_data
        print(request.POST)
    dictionary = dict()
    dictionary.update(main_form=locals()['main_form'])
    return render(request, 'Main.html', dictionary)
