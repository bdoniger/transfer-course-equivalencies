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

