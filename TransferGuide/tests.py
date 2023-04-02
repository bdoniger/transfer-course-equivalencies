from django.test import RequestFactory, TestCase
from .models import Course
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
class RequestValidity(TestCase):
    def test_CourseName(self):
    def test_CourseNumber(self):
    def test_CourseSubject(self):
    def test_university(self):
    def test_url(self):

