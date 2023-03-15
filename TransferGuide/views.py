from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout


def index(request):
    return render(request, 'TransferGuide/login.html')


def Info(request):
    return render(request, 'TransferGuide/ClassInfo.html')


def logoutt(request):
    logout(request)
    return render(request, 'TransferGuide/login.html')


