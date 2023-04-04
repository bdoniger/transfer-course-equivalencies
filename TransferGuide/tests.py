from django.test import RequestFactory, TestCase
from .models import Course, requestForm
from .views import SearchResultsView

'''
class CourseTests(TestCase):
    def test_Course_name(self):
        course = Course()
        name = course.courseName
        self.assertEqual(name, True)
'''


class URLTests(TestCase):
    def test_home(self):
        response = self.client.get('')
        self.assertTrue(response.status_code == 200)

    def test_All_Courses(self):
        response = self.client.get('/allCourses')
        self.assertTrue(response.status_code == 200)

    def test_Course_Search(self):
        response = self.client.get('/search/')
        self.assertTrue(response.status_code == 200)

    def test_Search(self):
        response = self.client.get('/search/')
        self.assertTrue(response.status_code == 200)

    def test_addEquivalentCourse(self):
        response = self.client.get('/addEquivalentCourse/')
        self.assertTrue(response.status_code == 200)

    def test_PendingRequests(self):
        response = self.client.get('/pendingRequests/')
        self.assertTrue(response.status_code == 200)

class CourseDisplay(TestCase):
    def test_display(self):
        course = Course(courseName="name", courseNumber='1', courseSubject='BRUH')
        name = course.courseName
        number = course.courseNumber
        subject = course.courseSubject
        self.assertEqual(subject + number + name, "BRUH" + "1" + "name")

    def test_display2(self):
        course = Course(courseName="name", courseNumber='123456', courseSubject='BRUH')
        name = course.courseName
        number = course.courseNumber
        subject = course.courseSubject
        self.assertEqual(subject + number + name, "BRUH" + "123456" + "name")

class Requests(TestCase):
    def test_request_creation(self):
        request = requestForm()
        name = request.courseName
        number = request.courseNumber
        subject = request.courseSubject
        self.assertEqual(name + number + subject, request.courseName + request.courseNumber + request.courseSubject)

    def test_request_creation2(self):
        request = requestForm(courseName="name", courseNumber="101", courseSubject="lol")
        name = request.courseName
        number = request.courseNumber
        subject = request.courseSubject
        self.assertEqual(name + number + subject, "name" + "101" + "lol")
