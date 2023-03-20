from django.db import models

# Create your models here.
class Course(models.Model): 
    courseName = models.CharField(max_length=200) #name of course
    courseNumber = models.CharField(max_length=5) #number of course
    courseSubject = models.CharField(max_length=20) #department of course, i.e. CS
    equivalentCourse = models.CharField(max_length=200) #equivalent UVA course
    def __str__(self):
        return self.courseName