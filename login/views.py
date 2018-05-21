from django.shortcuts import redirect


# Create your views here.
def login(request):
    return redirect('/accounts/login/')
