from django.shortcuts import redirect


def login(request):
    return redirect('/accounts/login/')
