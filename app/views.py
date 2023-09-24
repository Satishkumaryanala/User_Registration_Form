from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from app.forms import *


def registration(request):
    UFO = UserForm()
    PFO = ProfileForm()
    if request.method == 'POST' and request.FILES:
        UFDO = UserForm(request.POST)
        PFDO = ProfileForm(request.POST,request.FILES)
        if UFDO.is_valid() and PFDO.is_valid():
            MUFDO = UFDO.save(commit=False)
            MPFDO = PFDO.save(commit= False)

            MUFDO.set_password(UFDO.cleaned_data['password'])
            MUFDO.save()

            MPFDO.username = MUFDO
            MPFDO.save()
            return HttpResponse('<center><h1 style="color:green;">Registration done successfully</h1></center>')
            
        return HttpResponse('<center><h1 style="color:red;">Registration not done properly</h1></center>')
        

        return HttpResponse(str(UFDO))
    
    return render(request,'registration.html',{'UFO':UFO,'PFO':PFO})