from django.shortcuts import render
from django.core.mail import send_mail


from app.forms import *

# Create your views here.


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



    