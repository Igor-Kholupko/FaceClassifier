from django.shortcuts import redirect, render
from .models import Profile


def login(request):
    return redirect('/accounts/login/')


def general_statistics(request):
    users = Profile.objects.select_related('user')
    return render(request, 'general-stat.html', locals())

