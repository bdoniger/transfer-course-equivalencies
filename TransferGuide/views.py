import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.template import loader
from django.views import generic

from .tasks import sisBackground
from .models import Course
from django.shortcuts import redirect
import requests

from django.db.models import Q

from django.core import serializers

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


def make_query(subject_query, number_query, name_query, university_query):
    if (subject_query == '') & ((number_query == -1) | (number_query == '')) & (name_query == '') & (university_query == ''):
        return {}

    courses = Course.objects.all().order_by('courseSubject', 'courseNumber')
    subjects = Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()

    criteria = [subject_query, number_query, name_query, university_query]
    print(criteria)

    for i in range(len(criteria)):
        filter_criteria = criteria[i]
        if (filter_criteria is not None) & (filter_criteria != '') & (filter_criteria != -1):
            if filter_criteria == subject_query:
                courses = courses.filter(Q(courseSubject__icontains=filter_criteria))
                subjects = subjects.filter(Q(courseSubject__icontains=filter_criteria))
            elif filter_criteria == number_query:
                courses = courses.filter(Q(courseNumber__contains=number_query))
                subjects = subjects.filter(Q(courseNumber__contains=number_query))
            elif filter_criteria == name_query:
                courses = courses.filter(Q(courseName__icontains=name_query))
                subjects = subjects.filter(Q(courseName__icontains=name_query))
            elif filter_criteria == university_query:
                courses = courses.filter(Q(university__icontains=university_query))
                subjects = subjects.filter(Q(university__icontains=university_query))

    return {"courses": courses, "subjects": subjects}


class SearchResultsView(generic.ListView):
    model = Course
    template_name = 'TransferGuide/searchResults.html'
    context_object_name = 'all_courses_list'

    # Need to add search based on university once that is set up
    def get_queryset(self):
        subject_query = self.request.GET.get("subject")
        number_query = self.request.GET.get("number")
        name_query = self.request.GET.get("name")
        university_query = self.request.GET.get("university")
        if subject_query is None:
            subject_query = ''
        if subject_query is not None:
            subject_query = subject_query.upper()
        if name_query is None:
            name_query = ''
        if number_query is None:
            number_query = -1
        if university_query is None:
            university_query = ''

        return make_query(subject_query, number_query, name_query, university_query)


class CourseInfo(generic.ListView):
    model = Course
    template_name = 'TransferGuide/courseInfo.html'
    context_object_name = 'course_info'

    def get_queryset(self):
        subject_query = self.request.GET.get("subject")
        number_query = self.request.GET.get("number")
        queryset = Course.objects.filter(courseNumber=number_query, courseSubject=subject_query)
        return queryset


# maybe add approved/disapproved courses filter alter
class CourseFilter(generic.ListView):
    model = Course
    template_name = 'TransferGuide/newFilter.html'
    context_object_name = 'filtered_courses'

    def get_queryset(self):
        subject_query = self.request.GET.get("subject")
        number_query = self.request.GET.getlist("number")

        number_query = [eval(i) for i in number_query]

        if subject_query is None:
            subject_query = ''
        if number_query is None:
            number_query = -1
        subject_query = subject_query.split(',')
        number_query_list = []
        if len(number_query) > 0:
            number_query_list.append(min(number_query)*1000)
            for i in range(min(number_query)*1000, ((max(number_query)+1)*1000)-1):
                number_query_list.append(i)

        all_subjects_queryset = Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()

        all_subjects_queryset = all_subjects_queryset.values_list()
        subjects = []
        for item in all_subjects_queryset:
            if item[3] not in subjects:
                subjects.append(item[3])
        json_subjects = json.dumps(subjects)

        return_set = {
            "json": json_subjects,
            "courses": Course.objects.filter(
                Q(courseSubject__in=subject_query) & Q(courseNumber__in=number_query_list)),
            "filteredSubjects": Course.objects.filter(Q(courseSubject__in=subject_query) & Q(courseNumber__in=number_query_list)).values('courseSubject').order_by(
                'courseSubject').distinct(),
            "allSubjects": Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()
        }
        return return_set


class Test(generic.ListView):
    template_name = 'TransferGuide/test.html'
    context_object_name = 'all_courses_list'

    def get_queryset(self):
        return {
            "courses": Course.objects.all().order_by('courseSubject', 'courseNumber'),
            "subjects": Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()
        }
