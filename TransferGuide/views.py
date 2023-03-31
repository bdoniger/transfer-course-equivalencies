from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.template import loader
from django.views import generic

from .tasks import sisBackground
from .models import Course, requestForm
from django.shortcuts import redirect
import requests

from django.db.models import Q

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


class SearchResultsView(generic.ListView):
    model = Course
    template_name = 'TransferGuide/searchResults.html'
    context_object_name = 'all_courses_list'

    # Need to add search based on university once that is set up
    def get_queryset(self):
        subject_query = self.request.GET.get("subject")
        number_query = self.request.GET.get("number")
        name_query = self.request.GET.get("name")
        # print(subject_query, number_query, name_query)
        queryset = {}
        if subject_query is None:
            subject_query = ''
        if subject_query is not None:
            subject_query = subject_query.upper()
        if name_query is None:
            name_query = ''
        if number_query is None:
            number_query = -1

        # All 3 parameters so should be &
        if (subject_query != '') & (number_query != '') & (name_query != ''):
            queryset = {
                "courses": Course.objects.filter(
                    Q(courseSubject__icontains=subject_query) & Q(courseNumber__contains=number_query) & Q(
                        courseName__icontains=name_query))
                .order_by('courseSubject', 'courseNumber'),
                "subjects": Course.objects.filter(
                    Q(courseSubject__icontains=subject_query) & Q(courseNumber__contains=number_query) & Q(
                        courseName__icontains=name_query))
                .values('courseSubject').order_by('courseSubject').distinct()
            }

        # Subject and Number
        elif (subject_query != '') & (number_query != ''):
            queryset = {
                "courses": Course.objects.filter(
                    Q(courseSubject__icontains=subject_query) & Q(courseNumber__contains=number_query))
                .order_by('courseSubject', 'courseNumber'),
                "subjects": Course.objects.filter(
                    Q(courseSubject__icontains=subject_query) & Q(courseNumber__contains=number_query))
                .values('courseSubject').order_by('courseSubject').distinct()
            }

        # Subject and Name
        elif (subject_query != '') & (name_query != ''):
            queryset = {
                "courses": Course.objects.filter(
                    Q(courseSubject__icontains=subject_query) & Q(courseName__icontains=name_query))
                .order_by('courseSubject', 'courseNumber'),
                "subjects": Course.objects.filter(
                    Q(courseSubject__icontains=subject_query) & Q(courseName__icontains=name_query))
                .values('courseSubject').order_by('courseSubject').distinct()
            }

        # Number and Name
        elif (number_query != '') & (name_query != ''):
            queryset = {
                "courses": Course.objects.filter(
                    Q(courseNumber__contains=number_query) & Q(courseName__icontains=name_query))
                .order_by('courseSubject', 'courseNumber'),
                "subjects": Course.objects.filter(
                    Q(courseNumber__contains=number_query) & Q(courseName__icontains=name_query))
                .values('courseSubject').order_by('courseSubject').distinct()
            }
        # Just Subject
        elif subject_query != '':
            queryset = {
                "courses": Course.objects.filter(
                    Q(courseSubject__icontains=subject_query))
                .order_by('courseSubject', 'courseNumber'),
                "subjects": Course.objects.filter(
                    Q(courseSubject__icontains=subject_query))
                .values('courseSubject').order_by('courseSubject').distinct()
            }

        # Just Number
        elif number_query != '':
            queryset = {
                "courses": Course.objects.filter(
                    Q(courseNumber__contains=number_query))
                .order_by('courseSubject', 'courseNumber'),
                "subjects": Course.objects.filter(
                    Q(courseNumber__contains=number_query))
                .values('courseSubject').order_by('courseSubject').distinct()
            }

        # Just Name
        elif name_query != '':
            queryset = {
                "courses": Course.objects.filter(
                    Q(courseName__icontains=name_query))
                .order_by('courseSubject', 'courseNumber'),
                "subjects": Course.objects.filter(
                    Q(courseName__icontains=name_query))
                .values('courseSubject').order_by('courseSubject').distinct()
            }

        if queryset is not None:
            courses_got = queryset.get('courses')
            subjects_got = queryset.get('subjects')

            if (courses_got != '') & (courses_got is not None):
                courses_count = len(queryset.get('courses'))
            else:
                courses_count = 0
            if (subjects_got != '') & (subjects_got is not None):
                subjects_count = len(queryset.get('subjects'))
            else:
                subjects_count = 0

            if (courses_count == 0) & (subjects_count == 0):
                return {}
            else:
                return queryset
        else:
            return queryset


class CourseInfo(generic.ListView):
    model = Course
    template_name = 'TransferGuide/courseInfo.html'
    context_object_name = 'course_info'

    def get_queryset(self):
        subject_query = self.request.GET.get("subject")
        number_query = self.request.GET.get("number")
        name_query = self.request.GET.get("name")

        # name_query = name_query.replace('-', ' ')

        # print(subject_query, number_query, name_query)

        # queryset = Course.objects.filter(courseName__icontains=name_query, courseNumber=number_query, courseSubject=subject_query)
        queryset = Course.objects.filter(courseNumber=number_query, courseSubject=subject_query)
        # print(queryset)
        return queryset


# need to add university, maybe approved/disapproved courses filter alter
class CourseFilter(generic.ListView):
    model = Course
    template_name = 'TransferGuide/filter.html'
    context_object_name = 'filtered_courses'

    def get_queryset(self):
        subject_query = self.request.GET.getlist("subject")
        number_query = self.request.GET.getlist("number")

        print(number_query)
        number_query = [eval(i) for i in number_query]

        if subject_query is None:
            subject_query = ''
        if number_query is None:
            number_query = -1
        # subject_query_list = subject_query.split(',')
        print(subject_query)
        number_query_list = []
        if len(number_query) > 0:
            number_query_list.append(min(number_query) * 1000)
            for i in range(min(number_query) * 1000, ((max(number_query) + 1) * 1000) - 1):
                number_query_list.append(i)

        queryset = {
            "courses": Course.objects.filter(
                Q(courseSubject__in=subject_query) & Q(courseNumber__in=number_query_list)),
            "filteredSubjects": Course.objects.filter(courseSubject__in=subject_query).values('courseSubject').order_by(
                'courseSubject').distinct(),
            "allSubjects": Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()
        }
        print(queryset.get("courses"))
        return queryset


class RequestForms(generic.ListView):
    model = requestForm
    template_name = 'TransferGuide/Requests.html'



def Requestsdatabase(request):
    if(request.method == "POST"):

        #requestForm1 = requestForm.objects.create(title=request.POST['title'], body=request.POST['body'])

        return HttpResponse("d")