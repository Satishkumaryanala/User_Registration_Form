from django.shortcuts import render
from app.forms import * 
from django.core.mail import send_mail
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from app.models import *


# Create your views here.

def Home(request):
    if request.session.get('username'):
        UN = request.session.get('username')
        d={'UN':UN}
        return render(request,'Home.html',context=d)
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
            password = UFDO.cleaned_data['password']
            MUFDO.set_password(password)
            MUFDO.save()

            MPFDO = PFDO.save(commit=False)
            MPFDO.username = MUFDO
            MPFDO.save()

            send_mail(
                'Registration',
                'Registration done successfully',
                'pandurocky35@gmail.com',
                [MUFDO.email],
                fail_silently=False
            )

            return HttpResponse('<center><h1 style="color:green;">Registration Done successfully</h1></center>')

        return HttpResponse('Not valid properly')

    return render(request,'Register.html',d)


def User_login(request):
    if request.method=='POST':
        un = request.POST['un']
        pw = request.POST['pw']
        AUO = authenticate(username=un,password=pw)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=un

            return HttpResponseRedirect(reverse('Home'))

    return render(request,'User_login.html')

@login_required
def User_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Home'))

@login_required
def display_details(request):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    PO = Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_details.html',d)

@login_required
def change_password(request):
    if request.method == 'POST':
        password = request.POST['pw']
        Rpassword = request.POST['rpw']
        if password == Rpassword:
            un = request.session.get('username')
            UO = User.objects.get(username=un)
            UO.set_password(password)
            UO.save()
            return HttpResponse('<h1 style="color:green;">Password changed successfully</h1>')
        return HttpResponse('<h1 style="color: red;">password not matched</h1>')
    return render(request,'change_password.html')


def forget_password(request):
    if request.method == 'POST':
        username = request.POST['un']
        password = request.POST['pw']
        Rpassword = request.POST['rpw']

        UFO = User.objects.filter(username=username)

        if len(UFO)>0 and password==Rpassword:
            UO = UFO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('<h1 style="color:green;">Password changed successfully</h1>')
        return HttpResponse('<h1 style="color: red;">password not matched or Username not matched</h1>')
    return render(request,'forget_password.html')
