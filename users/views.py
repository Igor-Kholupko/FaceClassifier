from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.shortcuts import render, get_object_or_404
from workspace.models import ClassifiedByRelation
from .models import CustomUser


def login(request):
    return redirect('/accounts/login/')


def general_statistics(request):
    users = CustomUser.objects.all()
    return render(request, 'general-stat.html', locals())


def statistics_detail(request, pk):
    current_user = get_object_or_404(CustomUser, pk=pk)
    dirs = ClassifiedByRelation.objects.using('directories').filter(user_id=current_user.id)
    return render(request, 'statistics_detail.html', locals())
