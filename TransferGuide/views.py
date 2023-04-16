import json

import datetime

from django.db.models.functions import Length, Substr
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.contrib.auth import logout
from django.template import loader
from django.views import generic
from django.contrib import messages

from .tasks import sisBackground
from .models import Course, requestForm, Emails, AutoReplyEmail
from django.shortcuts import redirect
import requests

from django.db.models import Q

from django.core import serializers

subjectList = []


class index(generic.ListView):
    model = requestForm
    template_name = 'TransferGuide/newLogin.html'
    context_object_name = 'requestForm_list'


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


def addEquivCourse(request):
    if request.method == 'POST':
        form = request.POST

        existingCourse = Course.objects.filter(Q(universityLong__iexact=form.get('university')) | Q(
            universityShort__iexact=form.get('universityShort'))).filter(
            courseSubject=form.get('department')).filter(courseNumber=form.get('number'))

        if not existingCourse:
            # queryset is empty
            oCourse = Course()
            oCourse.courseName = form.get('name')
            oCourse.courseNumber = form.get('number')
            oCourse.courseSubject = form.get('department')
            oCourse.universityShort = form.get('universityShort')
            oCourse.universityLong = form.get('university')
            equivCourseDict = {
                "universityShort": "UVA",
                "universityLong": "University of Virginia",
                "subject": form.get('UVADepartment'),
                "number": form.get('UVANumber'),
                "name": form.get('UVAName')
            }
            equivCourseList = list()
            equivCourseList.append(equivCourseDict)
            oCourse.equivalentCourse = equivCourseList
            oCourse.save()

            # add outside course to uva course's equivalency list
            uvaCourse = Course.objects.filter(courseSubject=form.get('UVADepartment')).filter(
                courseNumber=form.get('UVANumber')).get()
            oldEquivList = uvaCourse.equivalentCourse
            UVAEquivCourseDict = {
                "universityShort": form.get('universityShort'),
                "universityLong": form.get('university'),
                "subject": form.get('department'),
                "number": form.get('number'),
                "name": form.get('name')
            }
            if (len(oldEquivList) == 0):
                oldEquivList = list()

            oldEquivList.append(UVAEquivCourseDict)
            uvaCourse.equivalentCourse = oldEquivList
            uvaCourse.save()

            messages.success(request, 'Course Equivalency Added!')
            return render(request, 'TransferGuide/newAddEquivCourse.html')
        else:
            messages.error(request, 'class equivalency already exists in database')
            return render(request, 'TransferGuide/newAddEquivCourse.html')

    return render(request, 'TransferGuide/newAddEquivCourse.html')


class CoursesViewAll(generic.ListView):
    template_name = 'TransferGuide/newAllCourses.html'
    context_object_name = 'all_courses_list'

    def get_queryset(self):
        return {
            "courses": Course.objects.all().order_by('courseSubject', 'courseNumber'),
            "subjects": Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()
        }


def make_query(subject_query, number_query, name_query, university_query):
    all_subjects_queryset = Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()
    all_universities_queryset = Course.objects.all().values('universityLong').order_by('universityLong').distinct()
    all_universities_short_queryset = Course.objects.all().values('universityShort').order_by('universityShort').distinct()
    all_numbers_queryset = Course.objects.all().values("courseNumber").order_by("courseNumber").distinct()
    all_names_queryset = Course.objects.all().values("courseName").order_by("courseName").distinct()

    all_subjects_queryset = all_subjects_queryset.values_list()
    all_universities_queryset = all_universities_queryset.values_list()
    all_universities_short_queryset = all_universities_short_queryset.values_list()
    all_numbers_queryset = all_numbers_queryset.values_list()
    all_names_queryset = all_names_queryset.values_list()
    subjects = []
    universities = []
    universities_short = []
    numbers = []
    names = []

    for item in all_subjects_queryset:
        if item[3] not in subjects:
            subjects.append(item[3])
    for item in all_universities_queryset:
        if item[5] not in universities:
            universities.append(item[5])
    for item in all_numbers_queryset:
        if item[2] not in numbers:
            numbers.append(item[2])
    for item in all_names_queryset:
        if item[1] not in names:
            if "\"" in item[1]:
                names.append(item[1].replace("\"", ''))
            else:
                names.append(item[1])
    for item in all_universities_short_queryset:
        if item[3] not in universities_short:
            universities_short.append(item[3])

    json_subjects = json.dumps(subjects)
    json_universities = json.dumps(universities)
    json_universities_short = json.dumps(universities_short)
    json_numbers = json.dumps(numbers)
    json_names = json.dumps(names)

    if (subject_query == '') & ((number_query == -1) | (number_query == '')) & (name_query == '') & (
            university_query == ''):
        return {"json": json_subjects, "universitiesJSON": json_universities, "universitiesShortJSON": json_universities_short, "numbersJSON": json_numbers,
                "namesJSON": json_names}

    courses = Course.objects.annotate(
        course_number_length=Length('courseNumber'),
        starting_digit=Substr('courseNumber', 1, 1),
    ).order_by('courseSubject', 'starting_digit', 'course_number_length', 'courseNumber')
    subjects = Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()

    criteria = [subject_query, number_query, name_query, university_query]

    for i in range(len(criteria)):
        filter_criteria = criteria[i]
        if (filter_criteria is not None) & (filter_criteria != '') & (filter_criteria != -1):
            if filter_criteria == subject_query:
                courses = courses.filter(Q(courseSubject__icontains=filter_criteria))
                subjects = subjects.filter(Q(courseSubject__icontains=filter_criteria))
            elif filter_criteria == number_query:
                courses &= courses.filter(Q(courseNumber=number_query))
                subjects &= subjects.filter(Q(courseNumber=number_query))
            elif filter_criteria == name_query:
                courses = courses.filter(Q(courseName__icontains=name_query))
                subjects = subjects.filter(Q(courseName__icontains=name_query))
            elif filter_criteria == university_query:
                courses = courses.filter(Q(universityLong__icontains=university_query))
                subjects = subjects.filter(Q(universityLong__icontains=university_query))

    return {"courses": courses, "subjects": subjects, "json": json_subjects, "universitiesJSON": json_universities,
            "universitiesShortJSON": json_universities_short, "numbersJSON": json_numbers, "namesJSON": json_names}


class SearchResultsView(generic.ListView):
    model = Course
    template_name = 'TransferGuide/newSearch.html'
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
    template_name = 'TransferGuide/newCourseInfo.html'
    context_object_name = 'course_info'

    def get_queryset(self):
        subject_query = self.request.GET.get("subject")
        number_query = self.request.GET.get("number")
        university_query = self.request.GET.get("university")

        queryset = Course.objects.filter(courseNumber=number_query, courseSubject=subject_query, universityShort__icontains=university_query)
        return queryset


def make_number_query(numbers):
    new_numbers = []
    for i in range(len(numbers)):
        num = numbers[i]
        tens = num * 10
        tens_upper = (num+1) * 10 - 1
        hundreds = num * 100
        hundreds_upper = (num+1) * 100 - 1
        thousands = num * 1000
        thousands_upper = (num+1) * 1000 - 1
        numbers_to_compute = [tens, tens_upper, hundreds, hundreds_upper, thousands, thousands_upper]
        index = 0
        while index < len(numbers_to_compute):
            lower = numbers_to_compute[index]
            index += 1
            upper = numbers_to_compute[index]
            index += 1
            for j in range(lower, upper+1):
                new_numbers.append(j)
    return new_numbers


# maybe add approved/disapproved courses filter alter
class CourseFilter(generic.ListView):
    model = Course
    template_name = 'TransferGuide/newFilter.html'
    context_object_name = 'filtered_courses'

    def get_queryset(self):
        subject_query = self.request.GET.get("subject")
        number_query = self.request.GET.get("number")
        university_query = self.request.GET.getlist("universities")
        if university_query == ['']:
            university_query = None
        # if subject_query is None:
        #     subject_query = ''
        # if (number_query == '') | (number_query is None):
        #     number_query = -1
        # if university_query is None:
        #     university_query = ''
        number_query_list = []
        subject_query = [subject_query]
        if not isinstance(number_query, int):
            if number_query is not None:
                number_query = list(number_query)
                count = number_query.count(',')
                for i in range(count):
                    number_query.remove(',')
                for i in range(len(number_query)):
                    if number_query[i] != '':
                        number_query[i] = eval(number_query[i])
                if len(number_query) > 0:
                    number_query_list = make_number_query(number_query)
        if subject_query == ' ':
            subject_query = None
        if university_query is not None:
            if len(university_query) > 0:
                university_query = university_query[0].split(',')
        if university_query == '':
            university_query = None
        if subject_query == ['']:
            subject_query = None
        if subject_query == [None]:
            subject_query = None
        if university_query == []:
            university_query = None

        all_subjects_queryset = Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()
        all_universities_queryset = Course.objects.all().values('universityLong').order_by('universityLong').distinct()

        all_subjects_queryset = all_subjects_queryset.values_list()
        all_universities_queryset = all_universities_queryset.values_list()
        subjects = []
        universities = []
        for item in all_subjects_queryset:
            if item[3] not in subjects:
                subjects.append(item[3])
        for item in all_universities_queryset:
            if item[5] not in universities:
                universities.append(item[5])
        json_subjects = json.dumps(subjects)
        json_universities = json.dumps(universities)

        filters = Q()
        if (subject_query != '') & (subject_query is not None):
            filters &= Q(courseSubject__in=subject_query)
        if len(number_query_list) > 0:
            filters &= Q(courseNumber__in=number_query_list)
        if university_query is not None:
            filters &= Q(universityLong__in=university_query)

        # courses = Course.objects.filter(
        #         Q(courseSubject__in=subject_query) & Q(courseNumber__in=number_query_list) & Q(
        #             universityLong__in=university_query)).order_by('courseNumber')
        if len(filters) < 1:
            courses = []
        else:
            courses = Course.objects.filter(
                filters).order_by('courseNumber')

        subjects = Course.objects.filter(
                filters).values('courseSubject').order_by(
                'courseSubject').distinct()

        if number_query is not None:
            courses = courses.annotate(
                course_number_length=Length('courseNumber'),
                starting_digit=Substr('courseNumber', 1, 1),
            ).order_by('courseSubject', 'starting_digit', 'course_number_length', 'courseNumber')

        return_set = {
            "json": json_subjects,
            "courses": courses,
            "filteredSubjects": subjects,
            "allSubjects": Course.objects.all().values('courseSubject').order_by('courseSubject').distinct(),
            "universitiesJSON": json_universities
        }
        return return_set


class AddEquivalency(generic.ListView):
    template_name = 'TransferGuide/newAddEquivCourse.html'
    context_object_name = 'all_courses_list'

    def get_queryset(self):
        all_subjects_queryset = Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()
        all_numbers_queryset = Course.objects.all().values("courseNumber").order_by("courseNumber").distinct()
        all_names_queryset = Course.objects.all().values("courseName").order_by("courseName").distinct()

        all_subjects_queryset = all_subjects_queryset.values_list()
        all_numbers_queryset = all_numbers_queryset.values_list()
        all_names_queryset = all_names_queryset.values_list()
        subjects = []
        numbers = []
        names = []

        for item in all_subjects_queryset:
            if item[4] == 'UVA':
                if item[3] not in subjects:
                    subjects.append(item[3])
        for item in all_numbers_queryset:
            if item[4] == 'UVA':
                if item[2] not in numbers:
                    numbers.append(item[2])
        for item in all_names_queryset:
            if item[4] == 'UVA':
                if item[1] not in names:
                    if "\"" in item[1]:
                        names.append(item[1].replace("\"", ''))
                    else:
                        names.append(item[1])

        json_subjects = json.dumps(subjects)
        json_numbers = json.dumps(numbers)
        json_names = json.dumps(names)
        return {"json": json_subjects, "numbersJSON": json_numbers, "namesJSON": json_names, "courses": all_subjects_queryset}


class Test(generic.ListView):
    template_name = 'TransferGuide/login.html'
    context_object_name = 'all_courses_list'

    def get_queryset(self):
        return {
            "courses": Course.objects.all().order_by('courseSubject', 'courseNumber'),
            "subjects": Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()
        }


class RequestForms(generic.ListView):
    model = requestForm
    template_name = 'TransferGuide/newRequests.html'


def requests_database(request):
    if request.method == "POST":
        requestForm1 = requestForm.objects.create(courseName=request.POST['courseName'],
                                                  courseNumber=request.POST['courseNumber'],
                                                  courseSubject=request.POST['courseSubject'],
                                                  university=request.POST['university'],
                                                  universityShort=request.POST['universityShort'],
                                                  url=request.POST['url'],
                                                  studentName=request.user,
                                                  studentEmail=request.user.email)
    return redirect('index')
    # return HttpResponseRedirect('https://transfer-credit-guide.herokuapp.com/')



# def autoEmail_database(request):
#     requests = requestForm.objects.all()
#
#     form_id = request.GET.get("request_id")
#     status = request.GET.get("status")
#
#     if form_id is not None:
#         form = requestForm.objects.all().filter(id=form_id)[0]
#         time = datetime.datetime.now()
#         content1 = "You class:" + request.GET.get("request_courseSubject") + request.GET.get("request_courseNumber") + request.GET.get("request_courseName") + " from " + request.GET.get("request_University") + " status from " + form.status + " to " + request.GET.get("status") + " at " + time.strftime("%Y-%m-%d %H:%M:%S")
#         autoReply = AutoReplyEmail.objects.create(content=content1, studentEmail=request.GET.get("request.studentEmail"))
#         form.status = status
#         form.save()
#
#     # return render(request, "TransferGuide/newPendingRequests.html", context={"requests": requests})


def pending_requests(request):
    # requests = requestForm.objects.all()

    requests = requestForm.objects.all()

    form_id = request.GET.get("request_id")
    status = request.GET.get("status")

    if form_id is not None:
        form = requestForm.objects.all().filter(id=form_id)[0]
        time = timezone.localtime()
        content1 = "You request form for: " + request.GET.get("request_courseSubject") + " " + request.GET.get(
            "request_courseNumber") + " " + request.GET.get("request_courseName") + " at " + request.GET.get(
            "request_University") + " has had its status changed from " + form.status + " to " + request.GET.get(
            "status") + " at " + time.strftime("%Y-%m-%d %H:%M:%S")
        autoReply = AutoReplyEmail.objects.create(content=content1,
                                                  studentEmail=request.GET.get("request.studentEmail"))
        form.status = status
        form.save()

    return render(request, "TransferGuide/newPendingRequests.html", context={"requests": requests})
    # return render(request, "TransferGuide/PendingRequests.html", context={"requests": requests})


def update_email_status(request, email_id):
    if request.method == 'POST':
        email = Emails.objects.get(id=email_id)
        email.status = request.POST.get('status')
        email.save()
        return redirect('mailBox')
    else:
        return HttpResponseNotAllowed(['POST'])


def mail_box(request):
    emails = Emails.objects.all()
    AutoReplys = AutoReplyEmail.objects.all()

    return render(request, "TransferGuide/newMailBox.html", context={"requests": emails, "Autos": AutoReplys})


def send_email(request):
    return render(request, "TransferGuide/newSendBox.html")


def email_database(request):
    if request.method == "POST":
        emailS1 = Emails.objects.create(title=request.POST['title'], content=request.POST['content'],
                                        studentName=request.user,
                                        studentEmail=request.user.email)
    # return HttpResponse("You Have submit your requests")
    return redirect('index')
