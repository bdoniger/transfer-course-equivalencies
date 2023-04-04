from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Course(models.Model):
    courseName = models.CharField(max_length=200, default="N/A")  # name of course
    courseNumber = models.CharField(max_length=5, default="N/A")  # number of course
    courseSubject = models.CharField(max_length=20, default="N/A")  # department of course, i.e. CS
    university = models.CharField(max_length=100, default="UVA")  # UVA or other
    equivalentCourse = models.JSONField(encoder=None, decoder=None, default=dict, null=True, blank=True)
    nonEquivalentCourse = models.JSONField(encoder=None, decoder=None, default=dict, null=True, blank=True)

    def __str__(self):
        return self.courseName


class requestForm(models.Model):
    courseName = models.CharField(max_length=200, default="N/A")  # name of course
    courseNumber = models.CharField(max_length=5, default="N/A")  # number of course
    courseSubject = models.CharField(max_length=20, default="N/A")  # department of course, i.e. CS
    university = models.CharField(max_length=100, default="N/A")  # UVA or other
    url = models.CharField(max_length=1000, default="N/A")  # url to class webpage
    studentName = models.ForeignKey(User, on_delete=models.CASCADE)
    studentEmail = models.CharField(max_length=1000, default="N/A")
    status = models.CharField(max_length=8, default="Pending")

    def __str__(self):
        return '{} {} {}, {}, {}, {}, {}, {}'.format(self.courseSubject, self.courseNumber,
                                                     self.courseName, self.university,
                                                     self.url, self.studentName, self.studentEmail, self.status)


class user(models.Model):
    isAdmin = models.BooleanField(default=True)