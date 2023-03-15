from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'TransferGuide/login.html')

def Info(request):
    return render(request, 'TransferGuide/ClassInfo.html')