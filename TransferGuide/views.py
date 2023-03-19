from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.template import loader
from django.views import generic

from .tasks import sisBackground
from django.db import models
from .models import Course
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import redirect
import requests

subjectList = []


def index(request):
    return render(request, 'TransferGuide/login.html')


def Info(request):
    return render(request, 'TransferGuide/ClassInfo.html')


def logoutt(request):
    logout(request)

    response = redirect('https://transfer-credit-guide.herokuapp.com/')
    return response
    # return render(request, 'TransferGuide/login.html')


def displayUpdate(request, semester, page, subjectNum):
    template = loader.get_template('TransferGuide/update.html')
    param = str(semester) + '/' + str(page) + '/' + str(subjectNum) + '/'
    num = (int(semester) * 202 + int(subjectNum)) * 100
    percent = int(num / 808)
    context = {
        'param': param,
        'percent': percent,
    }
    return HttpResponse(template.render(context, request))


def sisUpdate(request, semester, page, subjectNum):
    semesters = ['1231', '1232', '1236', '1238']
    semester = int(semester)
    subjectNum = int(subjectNum)
    page = int(page)
    if subjectList == []:
        info = requests.get(
            'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1232')
        data = info.json()
        a = data['subjects']

        gettingSubjects = True
        x = 0
        while gettingSubjects:
            try:
                subjects = a[x]
                subject = subjects['subject']
                subjectList.append(subject)
            except IndexError:
                print('done!')
                print(subjectList)
                gettingSubjects = False
                break

            x = x + 1

    test = sisBackground(semesters[semester], subjectList[subjectNum], page)

    if (test):
        subjectNum = subjectNum + 1
        page = 1
    else:
        page = page + 1

    if (subjectNum == len(subjectList)):
        subjectNum = 0
        page = 1
        semester = semester + 1

    if (semester == 4):
        return render(request, 'TransferGuide/ClassInfo.html')

    response = redirect('/displayUpdate/' + str(semester) + '/' + str(page) + '/' + str(subjectNum) + '/')
    return response
    # return render(request, 'TransferGuide/ClassInfo.html')


class CoursesViewAll(generic.ListView):
    template_name = 'TransferGuide/allCourses.html'
    context_object_name = 'all_courses_list'

    def get_queryset(self):
        return {
            "courses": Course.objects.all().order_by('courseSubject', 'courseNumber'),
            "subjects": Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()
        }
