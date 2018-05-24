from django.shortcuts import redirect, render
from .models import CustomUser


def login(request):
    return redirect('/accounts/login/')


def general_statistics(request):
    users = CustomUser.objects.all()
    return render(request, 'general-stat.html', locals())
