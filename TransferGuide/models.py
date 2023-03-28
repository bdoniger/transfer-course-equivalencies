from django.db import models

# Create your models here.
class Course(models.Model): 
    courseName = models.CharField(max_length=200, default="N/A") #name of course
    courseNumber = models.CharField(max_length=5, default="N/A") #number of course
    courseSubject = models.CharField(max_length=20, default="N/A") #department of course, i.e. CS
    university = models.CharField(max_length=100, default="UVA") #UVA or other
    #equivalentCourse = models.CharField(max_length=2000, default="N/A") #equivalent UVA course
    #nonEquvialentCourse = models.CharField(max_length=2000, default="N/A") #non-equivalent UVA course
    equivalentCourse = models.JSONField(encoder=None, decoder=None,default=dict)
    nonEquivalentCourse = models.JSONField(encoder=None, decoder=None,default=dict)

    def __str__(self):
        return self.courseName
    
class requestForm(models.Model):
    courseName = models.CharField(max_length=200, default="N/A") #name of course
    courseNumber = models.CharField(max_length=5, default="N/A") #number of course
    courseSubject = models.CharField(max_length=20, default="N/A") #department of course, i.e. CS
    university = models.CharField(max_length=100, default="N/A") #UVA or other
    url = models.CharField(max_length=1000, default="N/A") #url to class webpage