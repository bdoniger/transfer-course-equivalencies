from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout

import django_rq as RQ
from .tasks import sisBackground
=======
from django.db import models
from .models import Course
from django.core.exceptions import ObjectDoesNotExist 
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import redirect
import requests 


def index(request):
    return render(request, 'TransferGuide/login.html')


def Info(request):
    return render(request, 'TransferGuide/ClassInfo.html')


def logoutt(request):
    logout(request)

    response = redirect('https://transfer-credit-guide.herokuapp.com/')
    return response
    # return render(request, 'TransferGuide/login.html')

def sisUpdate(request):
    queue = RQ.get_queue('high')
    queue.enqueue(sisBackground)
    return render(request, 'TransferGuide/ClassInfo.html')
        

    
