from django.shortcuts import render
from django.core.mail import send_mail

from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from app.forms import *

# Create your views here.
def Home(request):
    if request.session.get('username'):
        UN = request.session.get('username')
        d={'UN':UN}
        return render(request,'Home.html',d)
    return render(request,'Home.html')

def Register(request):
    UFO = UserForm()
    PFO = ProfileForm()
    d={'UFO':UFO,'PFO':PFO}
    if request.method == 'POST' and request.FILES:
        UFDO = UserForm(request.POST)
        PFDO = ProfileForm(request.POST,request.FILES)
        if UFDO.is_valid() and PFDO.is_valid():
            MUFDO = UFDO.save(commit=False)
            MUFDO.save()

            MPFDO = PFDO.save(commit=False)
            MPFDO.username = MUFDO
            MPFDO.save()
            send_mail('Registration',
            'Registartion done successfully',
            'pandurocky35@gmail.com',
            [MUFDO.email],
            fail_silently=False
            )
            return HttpResponse('<center> Register successfully')
        return HttpResponse('valid error')
    return render(request,'Register.html',d)

def User_login(request):
    if request.method=='POST':
        username = request.POST['un']
        password = request.POST['pw']
        AUO = authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('Home'))
        else:
            return HttpResponse('NOT DONE')

    return render(request,'User_login.html')

@login_required
def User_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Home'))

    