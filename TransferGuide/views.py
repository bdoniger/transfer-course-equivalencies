import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout
from django.template import loader
from django.views import generic
from django.contrib import messages

from .tasks import sisBackground
from .models import Course, requestForm
from django.shortcuts import redirect
import requests

from django.db.models import Q

from django.core import serializers

subjectList = []


class index(generic.ListView):
    model = requestForm
    template_name = 'TransferGuide/newLogin.html'
    context_object_name = 'requestForm_list'


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


def addEquivCourse(request):
    if request.method == 'POST':
        form = request.POST

        existingCourse = Course.objects.filter(university=form.get('university')).filter(
            courseSubject=form.get('department')).filter(courseNumber=form.get('number'))

        if not existingCourse:
            # queryset is empty
            oCourse = Course()
            oCourse.courseName = form.get('name')
            oCourse.courseNumber = form.get('number')
            oCourse.courseSubject = form.get('department')
            oCourse.university = form.get('university')
            equivCourseDict = {
                "university": "UVA",
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
                "university": form.get('university'),
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
            return render(request, 'TransferGuide/addEquivCourse.html')
        else:
            messages.error(request, 'class equivalency already exists in database')
            return render(request, 'TransferGuide/addEquivCourse.html')

    return render(request, 'TransferGuide/addEquivCourse.html')


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
    all_universities_queryset = Course.objects.all().values('university').order_by('university').distinct()
    all_numbers_queryset = Course.objects.all().values("courseNumber").order_by("courseNumber").distinct()
    all_names_queryset = Course.objects.all().values("courseName").order_by("courseName").distinct()

    all_subjects_queryset = all_subjects_queryset.values_list()
    all_universities_queryset = all_universities_queryset.values_list()
    all_numbers_queryset = all_numbers_queryset.values_list()
    all_names_queryset = all_names_queryset.values_list()
    subjects = []
    universities = []
    numbers = []
    names = []

    for item in all_subjects_queryset:
        if item[3] not in subjects:
            subjects.append(item[3])
    for item in all_universities_queryset:
        if item[4] not in universities:
            universities.append(item[4])
    for item in all_numbers_queryset:
        if item[2] not in numbers:
            numbers.append(item[2])
    for item in all_names_queryset:
        if item[1] not in names:
            if "\"" in item[1]:
                names.append(item[1].replace("\"", ''))
            else:
                names.append(item[1])

    json_subjects = json.dumps(subjects)
    json_universities = json.dumps(universities)
    json_numbers = json.dumps(numbers)
    json_names = json.dumps(names)

    if (subject_query == '') & ((number_query == -1) | (number_query == '')) & (name_query == '') & (
            university_query == ''):
        return {"json": json_subjects, "universitiesJSON": json_universities, "numbersJSON": json_numbers,
                "namesJSON": json_names}

    courses = Course.objects.all().order_by('courseSubject', 'courseNumber')
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
                courses = courses.filter(Q(university__icontains=university_query))
                subjects = subjects.filter(Q(university__icontains=university_query))

    return {"courses": courses, "subjects": subjects, "json": json_subjects, "universitiesJSON": json_universities,
            "numbersJSON": json_numbers, "namesJSON": json_names}


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
        number_query = self.request.GET.get("number")
        university_query = self.request.GET.getlist("universities")

        if subject_query is None:
            subject_query = ''
        if (number_query == '') | (number_query is None):
            number_query = -1
        if university_query is None:
            university_query = ''
        number_query_list = []
        if not isinstance(number_query, int):
            number_query = list(number_query)
            count = number_query.count(',')
            for i in range(count):
                number_query.remove(',')
            for i in range(len(number_query)):
                if number_query[i] != '':
                    number_query[i] = eval(number_query[i])
            if len(number_query) > 0:
                number_query_list.append(min(number_query) * 1000)
                lower_bound = min(number_query) * 1000
                upper_bound = (max(number_query) + 1) * 1000
                for i in range(lower_bound, upper_bound, 1):
                    number_query_list.append(i)

        subject_query = subject_query.split(',')

        all_subjects_queryset = Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()
        all_universities_queryset = Course.objects.all().values('university').order_by('university').distinct()

        all_subjects_queryset = all_subjects_queryset.values_list()
        all_universities_queryset = all_universities_queryset.values_list()
        subjects = []
        universities = []
        for item in all_subjects_queryset:
            if item[3] not in subjects:
                subjects.append(item[3])
        for item in all_universities_queryset:
            if item[4] not in universities:
                universities.append(item[4])
        json_subjects = json.dumps(subjects)
        json_universities = json.dumps(universities)

        return_set = {
            "json": json_subjects,
            "courses": Course.objects.filter(
                Q(courseSubject__in=subject_query) & Q(courseNumber__in=number_query_list) & Q(
                    university__in=university_query)),
            "filteredSubjects": Course.objects.filter(
                Q(courseSubject__in=subject_query) & Q(courseNumber__in=number_query_list) & Q(
                    university__in=university_query)).values('courseSubject').order_by(
                'courseSubject').distinct(),
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
        return {"json": json_subjects, "numbersJSON": json_numbers, "namesJSON": json_names}


class Test(generic.ListView):
    template_name = 'TransferGuide/newAddEquivCourse.html'
    context_object_name = 'all_courses_list'

    def get_queryset(self):
        return {
            "courses": Course.objects.all().order_by('courseSubject', 'courseNumber'),
            "subjects": Course.objects.all().values('courseSubject').order_by('courseSubject').distinct()
        }


class RequestForms(generic.ListView):
    model = requestForm
    template_name = 'TransferGuide/Requests.html'


def requests_database(request):
    if request.method == "POST":
        requestForm1 = requestForm.objects.create(courseName=request.POST['courseName'],
                                                  courseNumber=request.POST['courseNumber'],
                                                  courseSubject=request.POST['courseSubject'],
                                                  university=request.POST['university'], url=request.POST['url'],
                                                  studentName=request.user, studentEmail=request.user.email)

        return HttpResponse("You Have submit your requests")
