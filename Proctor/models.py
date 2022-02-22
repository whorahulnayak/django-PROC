from tokenize import Name
from django.db import models

from proctoring.settings import MEDIA_ROOT, MEDIA_URL

# Create your models here.

class Student(models.Model):
    USN = models.CharField(max_length=10, blank = True, null = True)
    DoB = models.CharField(max_length=12, blank = True, null = True)
    Blood = models.CharField(max_length=3, blank = True, null = True)
    Phone = models.IntegerField(blank = True, null = True)
    EmailId = models.EmailField(max_length=100)
    Name = models.TextField(max_length=70, blank = True, null = True)
    Proctor = models.TextField(max_length=70, blank = True, null = True)
    Password = models.CharField(max_length=50)
    Branch = models.TextField(max_length=4, blank = True, null = True)
    Profilepic = models.ImageField(upload_to="students", blank = True, null = True)
    Semester = models.IntegerField(blank = True, null = True)
    Section = models.TextField(max_length=1, blank = True, null = True)
    Semester1 = models.CharField(max_length=100, blank = True, null = True)
    Semester2 = models.CharField(max_length=100, blank = True, null = True)
    Semester3 = models.CharField(max_length=100, blank = True, null = True)
    Semester4 = models.CharField(max_length=100, blank = True, null = True)
    Semester5 = models.CharField(max_length=100, blank = True, null = True)
    Semester6 = models.CharField(max_length=100, blank = True, null = True)
    Semester7 = models.CharField(max_length=100, blank = True, null = True)
    Semester8 = models.CharField(max_length=100, blank = True, null = True)
    Activitypts = models.IntegerField(default=0)
    Archived = models.TextField(max_length=5, default="no")

    def __str__(self):
        return self.EmailId

class Proctor(models.Model):
    ProctorId = models.CharField(max_length=10)
    Name = models.TextField(max_length=70)
    EmailId = models.EmailField(max_length=100)
    Password = models.CharField(max_length=50)
    Department = models.TextField(max_length=3, default="ISE")
    Profilepic = models.ImageField(upload_to="proctors", blank = True, null = True)

    def __str__(self):
        return self.EmailId
        
class Coordinator(models.Model):
    pass

class Announcements(models.Model):
    AnnouncedBy = models.EmailField(max_length=100)
    Heading = models.TextField(max_length=25)
    Desc = models.TextField(max_length=300)
    Link = models.TextField(max_length=75,default="",blank = True, null = True)
    Date = models.DateField(auto_now_add=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.Heading
        
class Semrec1(models.Model):
    USN = models.CharField(max_length=10,blank = True, null = True)
    Name = models.TextField(max_length=70,blank = True, null = True)
    EmailId = models.EmailField(max_length=100,blank = True, null = True)
    Course1 = models.TextField(max_length=34,blank = True, null = True)
    Course2 = models.TextField(max_length=34,blank = True, null = True)
    Course3 = models.TextField(max_length=34,blank = True, null = True)
    Course4 = models.TextField(max_length=34,blank = True, null = True)
    Course5 = models.TextField(max_length=34,blank = True, null = True)
    Course6 = models.TextField(max_length=34,blank = True, null = True)
    Course7 = models.TextField(max_length=34,blank = True, null = True)
    Course8 = models.TextField(max_length=34,blank = True, null = True)
    Course9 = models.TextField(max_length=34,blank = True, null = True)
    Course10 = models.TextField(max_length=34,blank = True, null = True)
    Result = models.FileField(upload_to="results", blank = True, null = True)
    SGPA = models.FloatField(blank = True, null = True)

    def __str__(self):
        return self.USN

class Semrec2(models.Model):
    USN = models.CharField(max_length=10,blank = True, null = True)
    Name = models.TextField(max_length=70,blank = True, null = True)
    EmailId = models.EmailField(max_length=100,blank = True, null = True)
    Course1 = models.TextField(max_length=34,blank = True, null = True)
    Course2 = models.TextField(max_length=34,blank = True, null = True)
    Course3 = models.TextField(max_length=34,blank = True, null = True)
    Course4 = models.TextField(max_length=34,blank = True, null = True)
    Course5 = models.TextField(max_length=34,blank = True, null = True)
    Course6 = models.TextField(max_length=34,blank = True, null = True)
    Course7 = models.TextField(max_length=34,blank = True, null = True)
    Course8 = models.TextField(max_length=34,blank = True, null = True)
    Course9 = models.TextField(max_length=34,blank = True, null = True)
    Course10 = models.TextField(max_length=34,blank = True, null = True)
    Result = models.FileField(upload_to="results", blank = True, null = True)
    SGPA = models.FloatField(blank = True, null = True)

    def __str__(self):
        return self.USN
    
class Semrec3(models.Model):
    USN = models.CharField(max_length=10,blank = True, null = True)
    Name = models.TextField(max_length=70,blank = True, null = True)
    EmailId = models.EmailField(max_length=100,blank = True, null = True)
    Course1 = models.TextField(max_length=34,blank = True, null = True)
    Course2 = models.TextField(max_length=34,blank = True, null = True)
    Course3 = models.TextField(max_length=34,blank = True, null = True)
    Course4 = models.TextField(max_length=34,blank = True, null = True)
    Course5 = models.TextField(max_length=34,blank = True, null = True)
    Course6 = models.TextField(max_length=34,blank = True, null = True)
    Course7 = models.TextField(max_length=34,blank = True, null = True)
    Course8 = models.TextField(max_length=34,blank = True, null = True)
    Course9 = models.TextField(max_length=34,blank = True, null = True)
    Course10 = models.TextField(max_length=34,blank = True, null = True)
    Result = models.FileField(upload_to="results", blank = True, null = True)
    SGPA = models.FloatField(blank = True, null = True)

    def __str__(self):
        return self.USN

class Semrec4(models.Model):
    USN = models.CharField(max_length=10,blank = True, null = True)
    Name = models.TextField(max_length=70,blank = True, null = True)
    EmailId = models.EmailField(max_length=100,blank = True, null = True)
    Course1 = models.TextField(max_length=34,blank = True, null = True)
    Course2 = models.TextField(max_length=34,blank = True, null = True)
    Course3 = models.TextField(max_length=34,blank = True, null = True)
    Course4 = models.TextField(max_length=34,blank = True, null = True)
    Course5 = models.TextField(max_length=34,blank = True, null = True)
    Course6 = models.TextField(max_length=34,blank = True, null = True)
    Course7 = models.TextField(max_length=34,blank = True, null = True)
    Course8 = models.TextField(max_length=34,blank = True, null = True)
    Course9 = models.TextField(max_length=34,blank = True, null = True)
    Course10 = models.TextField(max_length=34,blank = True, null = True)
    Result = models.FileField(upload_to="results", blank = True, null = True)
    SGPA = models.FloatField(blank = True, null = True)

    def __str__(self):
        return self.USN

class Semrec5(models.Model):
    USN = models.CharField(max_length=10,blank = True, null = True)
    Name = models.TextField(max_length=70,blank = True, null = True)
    EmailId = models.EmailField(max_length=100,blank = True, null = True)
    Course1 = models.TextField(max_length=34,blank = True, null = True)
    Course2 = models.TextField(max_length=34,blank = True, null = True)
    Course3 = models.TextField(max_length=34,blank = True, null = True)
    Course4 = models.TextField(max_length=34,blank = True, null = True)
    Course5 = models.TextField(max_length=34,blank = True, null = True)
    Course6 = models.TextField(max_length=34,blank = True, null = True)
    Course7 = models.TextField(max_length=34,blank = True, null = True)
    Course8 = models.TextField(max_length=34,blank = True, null = True)
    Course9 = models.TextField(max_length=34,blank = True, null = True)
    Course10 = models.TextField(max_length=34,blank = True, null = True)
    Result = models.FileField(upload_to="results", blank = True, null = True)
    SGPA = models.FloatField(blank = True, null = True)

    def __str__(self):
        return self.USN

class Semrec6(models.Model):
    USN = models.CharField(max_length=10,blank = True, null = True)
    Name = models.TextField(max_length=70,blank = True, null = True)
    EmailId = models.EmailField(max_length=100,blank = True, null = True)
    Course1 = models.TextField(max_length=34,blank = True, null = True)
    Course2 = models.TextField(max_length=34,blank = True, null = True)
    Course3 = models.TextField(max_length=34,blank = True, null = True)
    Course4 = models.TextField(max_length=34,blank = True, null = True)
    Course5 = models.TextField(max_length=34,blank = True, null = True)
    Course6 = models.TextField(max_length=34,blank = True, null = True)
    Course7 = models.TextField(max_length=34,blank = True, null = True)
    Course8 = models.TextField(max_length=34,blank = True, null = True)
    Course9 = models.TextField(max_length=34,blank = True, null = True)
    Course10 = models.TextField(max_length=34,blank = True, null = True)
    Result = models.FileField(upload_to="results", blank = True, null = True)
    SGPA = models.FloatField(blank = True, null = True)

    def __str__(self):
        return self.USN

class Semrec7(models.Model):
    USN = models.CharField(max_length=10,blank = True, null = True)
    Name = models.TextField(max_length=70,blank = True, null = True)
    EmailId = models.EmailField(max_length=100,blank = True, null = True)
    Course1 = models.TextField(max_length=34,blank = True, null = True)
    Course2 = models.TextField(max_length=34,blank = True, null = True)
    Course3 = models.TextField(max_length=34,blank = True, null = True)
    Course4 = models.TextField(max_length=34,blank = True, null = True)
    Course5 = models.TextField(max_length=34,blank = True, null = True)
    Course6 = models.TextField(max_length=34,blank = True, null = True)
    Course7 = models.TextField(max_length=34,blank = True, null = True)
    Course8 = models.TextField(max_length=34,blank = True, null = True)
    Course9 = models.TextField(max_length=34,blank = True, null = True)
    Course10 = models.TextField(max_length=34,blank = True, null = True)
    Result = models.FileField(upload_to="results", blank = True, null = True)
    SGPA = models.FloatField(blank = True, null = True)

    def __str__(self):
        return self.USN

class Semrec8(models.Model):
    USN = models.CharField(max_length=10,blank = True, null = True)
    Name = models.TextField(max_length=70,blank = True, null = True)
    EmailId = models.EmailField(max_length=100,blank = True, null = True)
    Course1 = models.TextField(max_length=34,blank = True, null = True)
    Course2 = models.TextField(max_length=34,blank = True, null = True)
    Course3 = models.TextField(max_length=34,blank = True, null = True)
    Course4 = models.TextField(max_length=34,blank = True, null = True)
    Course5 = models.TextField(max_length=34,blank = True, null = True)
    Course6 = models.TextField(max_length=34,blank = True, null = True)
    Course7 = models.TextField(max_length=34,blank = True, null = True)
    Course8 = models.TextField(max_length=34,blank = True, null = True)
    Course9 = models.TextField(max_length=34,blank = True, null = True)
    Course10 = models.TextField(max_length=34,blank = True, null = True)
    Result = models.FileField(upload_to="results", blank = True, null = True)
    SGPA = models.FloatField(blank = True, null = True)

    def __str__(self):
        return self.USN

class Activities(models.Model):
    Proctor = models.TextField(max_length=70, blank = True, null = True)
    USN = models.CharField(max_length=10, blank = True, null = True)
    Name = models.TextField(max_length=30, blank = True, null = True)
    EmailId = models.EmailField(max_length=100)
    Actname = models.TextField(max_length=70, blank = True, null = True)
    Actdesc = models.TextField(max_length=100, blank = True, null = True)
    Actimg = models.ImageField(upload_to="activities/images", blank = True, null = True)
    Actreport = models.FileField(upload_to="activities/reports", blank = True, null = True)
    Actdate = models.DateField(auto_now_add=True)
    Actpts = models.IntegerField(default=0)
    Acttype = models.TextField(max_length=30, blank = True, null = True)
    Actduration = models.TextField(max_length=10, blank = True, null = True)
    Reject = models.TextField(max_length=1, default="N")

    def __str__(self):
        return self.USN

class Notifications(models.Model):
    Proctor = models.TextField(max_length=70, blank = True, null = True)
    EmailId = models.EmailField(max_length=100, blank = True, null = True)
    Nottype = models.TextField(max_length=100, blank = True, null = True)
    Notification = models.TextField(max_length=100, blank = True, null = True)
    Date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Proctor + "(" + str(self.Date.date()) + ")"

class Supplementary(models.Model):
    USN = models.CharField(max_length=10,blank = True, null = True)
    Name = models.TextField(max_length=70,blank = True, null = True)
    EmailId = models.EmailField(max_length=100,blank = True, null = True)
    Semester = models.IntegerField(default=0)
    Courses = models.CharField(max_length=100, blank = True, null = True)
    Course1 = models.TextField(max_length=34,blank = True, null = True)
    Course2 = models.TextField(max_length=34,blank = True, null = True)
    Course3 = models.TextField(max_length=34,blank = True, null = True)
    Course4 = models.TextField(max_length=34,blank = True, null = True)
    Course5 = models.TextField(max_length=34,blank = True, null = True)
    Course6 = models.TextField(max_length=34,blank = True, null = True)
    Course7 = models.TextField(max_length=34,blank = True, null = True)
    Course8 = models.TextField(max_length=34,blank = True, null = True)
    Course9 = models.TextField(max_length=34,blank = True, null = True)
    Course10 = models.TextField(max_length=34,blank = True, null = True)
    Result = models.FileField(upload_to="results", blank = True, null = True)
    SGPA = models.FloatField(blank = True, null = True)

    def __str__(self):
        return self.USN + "(" + str(self.Semester) + ")"

class Bugs(models.Model):
    EmailId = models.EmailField(max_length=100,blank = True, null = True)
    Name = models.TextField(max_length=70,blank = True, null = True)
    Bugdesc = models.TextField(max_length=300,blank = True, null = True)
    Priority = models.TextField(max_length=10,blank = True, null = True)
    Bugimg = models.ImageField(upload_to="bugs", blank = True, null = True)
    Date = models.DateTimeField(auto_now=True)

class Requests(models.Model):
    EmailId = models.EmailField(max_length=100,blank = True, null = True)
    USN = models.CharField(max_length=10,blank = True, null = True)
    Rec = models.TextField(max_length=10,blank = True, null = True)
    Other = models.TextField(max_length=30,blank = True, null = True)
    Date = models.DateTimeField(auto_now=True)