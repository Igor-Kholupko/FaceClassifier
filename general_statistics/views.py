from django.shortcuts import render
from .models import Profile


def general_statistics(request):
    users = Profile.objects.all()
    return render(request, 'general-stat.html', locals())

