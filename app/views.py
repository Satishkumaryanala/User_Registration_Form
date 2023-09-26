from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from app.forms import *

def InsertData(request):
    TFO = TopicForm()
    WFO = WebpageForm()
    AFO = AccessRecordForm()

    d={'TFO':TFO,'WFO':WFO,'AFO': AFO}

    if request.method == 'POST':
        TFDO = TopicForm(request.POST)
        WFDO = WebpageForm(request.POST)
        AFDO = AccessRecordForm(request.POST)
        if TFDO.is_valid() and WFDO.is_valid() and AFDO.is_valid():
            MTFDO = TFDO.save(commit=False)
            MTFDO.save()

            MWFDO = WFDO.save(commit=False)
            MWFDO.topic_name = MTFDO
            MWFDO.save()

            MAFDO = AFDO.save(commit=False)
            MAFDO.name = MWFDO
            MAFDO.save()

            return HttpResponse('<center><h1 style="color:green;">Data inserted to Models Successfully</h1></center>')

        return HttpResponse('<center><h1 style="color:red;">Validation error occured</h1></center>')

    return render(request,'InsertData.html',d)

