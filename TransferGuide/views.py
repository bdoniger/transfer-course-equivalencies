from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
import django_rq as RQ
from .tasks import sisBackground

def index(request):
    return render(request, 'TransferGuide/login.html')


def Info(request):
    return render(request, 'TransferGuide/ClassInfo.html')


def logoutt(request):
    logout(request)
    return render(request, 'TransferGuide/login.html')

def sisUpdate(request):
    queue = RQ.get_queue('high')
    queue.enqueue(sisBackground)
    return render(request, 'TransferGuide/ClassInfo.html')
        

    
