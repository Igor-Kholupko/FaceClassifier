from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.shortcuts import render, get_object_or_404
from workspace.models import Directory, ClassifiedByRelation
from .models import CustomUser


def login(request):
    return redirect('/accounts/login/')


def general_statistics(request):
    users = CustomUser.objects.all()
    dirs_all = Directory.objects.using('directories').count()
    dirs_classified = Directory.objects.using('directories').exclude(classifications_amount=0).count()
    percent = dirs_classified/dirs_all*100
    return render(request, 'general-stat.html', locals())


def statistics_detail(request, pk):
    current_user = get_object_or_404(CustomUser, pk=pk)
    dirs = ClassifiedByRelation.objects.using('directories').filter(user_id=current_user.id)
    return render(request, 'statistics_detail.html', locals())
