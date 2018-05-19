from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def workspace(request):
    return render(request, 'Main.html', locals())
