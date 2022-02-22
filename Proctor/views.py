from datetime import date, datetime
from email import message
from itertools import chain
from django.http import HttpResponse, request
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import string
import random

from proctoring.settings import EMAIL_HOST_USER
from .models import (Notifications, Student, Proctor, Announcements, 
Coordinator, Semrec1, Semrec2, Semrec3, Semrec4, Semrec5, Semrec6, 
Semrec7, Semrec8, Activities, Supplementary)

# Create your views here.

def Login1(request):
    return render(request, 'Login/Login1.html')

def Login2(request):
    return render(request, 'Login/Login2.html')

def Login3(request):
    return render(request, 'Login/Login3.html')

def Login4(request):
    return redirect('admin/')
    #return render(request, 'Login/Login4.html')

def SignUp(request):
    return render(request, 'Login/Signup.html')

def SignupSuccess(request):
    if request.method == 'POST':
        enteremailid = request.POST.get("mailid")
        enterpass = request.POST.get("password")
        roleKey = request.POST.get("rolekey")
    if enteremailid[-11:] != 'bmsce.ac.in':
        messages.error(request, "External mail id detected")
        return render(request, 'Login/Signup.html')
    if Student.objects.filter(EmailId=enteremailid) or Proctor.objects.filter(EmailId=enteremailid):
        messages.error(request, "Profile already exists")
        return render(request, 'Login/Signup.html')
    else:
        if roleKey == "s20BMSis24":
            # create a user in student table
            request.session['sUserMailId'] = enteremailid
            request.session['sUserPassword'] = enterpass
            newObject = Student(EmailId=enteremailid, Password=enterpass)
            newObject.save()
            proctors = Proctor.objects.all()
            messages.success(request, "Profile has been created")
            return render(request, 'Login/SignupDetails.html', {"proctorlist": proctors})
        elif roleKey == "p_BMSis_":
            # create a user in proctor table
            request.session['UserMailId'] = enteremailid
            request.session['UserPassword'] = enterpass
            newObject = Proctor(EmailId=enteremailid, Password=enterpass)
            newObject.save()
            messages.success(request, "Profile has been created")
            return redirect('ProctorLogin')
        elif roleKey == "co_BMSis_":
            # create a user in coordinator table
            messages.success(request, "Profile has been created")
            return render(request, 'Home/coordinator/dashboard.html')
        else:
            messages.error(request, "Invalid Role Key")
            return render(request, 'Login/Signup.html')

def SignupDetails(request):
    newObject = Student.objects.get(EmailId=request.session['sUserMailId'], Password=request.session['sUserPassword'])
    if request.method == 'POST':
        if request.POST.get('name'):
            newObject.Name = request.POST.get('name').title()
        if request.POST.get('USN'):
            newObject.USN = request.POST.get('USN').upper()
        if request.POST.get('blood'):
            newObject.Blood = request.POST.get('blood')
        if request.POST.get('proctor'):
            newObject.Proctor = request.POST.get('proctor').lower()
        if request.POST.get('semester'):
            newObject.Semester = request.POST.get('semester')
        if request.POST.get('branch'):
            newObject.Branch = request.POST.get('branch').upper()
        if request.POST.get('section'):
            newObject.Section = request.POST.get('section').upper()
        if request.POST.get('dob'):
            newObject.DoB = request.POST.get('dob')
        if request.POST.get('phone'):
            newObject.Phone = request.POST.get('phone')
        newObject.save()
        if request.POST.get('proctor') and request.POST.get('branch'):
            a = Semrec1(EmailId=request.session['sUserMailId'],USN=request.POST.get('USN').upper(),Name=request.POST.get('name').capitalize())
            b = Semrec2(EmailId=request.session['sUserMailId'],USN=request.POST.get('USN').upper(),Name=request.POST.get('name').capitalize())
            c = Semrec3(EmailId=request.session['sUserMailId'],USN=request.POST.get('USN').upper(),Name=request.POST.get('name').capitalize())
            d = Semrec4(EmailId=request.session['sUserMailId'],USN=request.POST.get('USN').upper(),Name=request.POST.get('name').capitalize())
            e = Semrec5(EmailId=request.session['sUserMailId'],USN=request.POST.get('USN').upper(),Name=request.POST.get('name').capitalize())
            f = Semrec6(EmailId=request.session['sUserMailId'],USN=request.POST.get('USN').upper(),Name=request.POST.get('name').capitalize())
            g = Semrec7(EmailId=request.session['sUserMailId'],USN=request.POST.get('USN').upper(),Name=request.POST.get('name').capitalize())
            h = Semrec8(EmailId=request.session['sUserMailId'],USN=request.POST.get('USN').upper(),Name=request.POST.get('name').capitalize())
            a.save()
            b.save()
            c.save()
            d.save()
            e.save()
            f.save()
            g.save()
            h.save()
            newNot = Notifications(EmailId=request.session['sUserMailId'],
            Proctor=request.POST.get('proctor').lower(),
            Nottype="New student",
            Notification=request.POST.get('USN').upper())
            newNot.save()
        else:
            newNot = Notifications(EmailId=request.session['sUserMailId'],
            Proctor=newObject.Proctor,
            Nottype="Record update",
            Notification=newObject.USN)
            newNot.save()
    messages.success(request, 'Record updated successfully')
    return redirect('StudentLogin')

def StudentLogin(request):
    if request.method == 'POST':
        enteremailid = request.POST.get("mailid")
        request.session['sUserMailId'] = enteremailid
        enterpass = request.POST.get("password")
        request.session['sUserPassword'] = enterpass
    if 'sUserMailId' not in request.session:
        messages.error(request, "Session timed out")
        return redirect('Login2')
    if Student.objects.filter(EmailId=request.session['sUserMailId'], Password=request.session['sUserPassword']):
        details = Student.objects.get(EmailId=request.session['sUserMailId'])
        if (details.USN is None or details.Proctor is None or details.Branch is None or details.Semester is None or details.Section is None or details.Name is None):
            proctors = Proctor.objects.all()
            return render(request, 'Login/SignupDetails.html', {"proctorlist": proctors})
        else:
            context = {"mailid": request.session['sUserMailId'],"USN": details.USN.upper(),"Pname": details.Proctor.upper(),
            "Branch": details.Branch.upper(),"Semester": details.Semester,"Section": details.Section.upper(),"Name": details.Name.title(),
            }
            if details.Profilepic:
                Profilepic = {
                    "Profilepic": details.Profilepic
                }
                context.update(Profilepic)
            if details.Proctor:
                allannouncements = Announcements.objects.filter(AnnouncedBy=details.Proctor).order_by('-id')
                announcements = {"announcement": allannouncements}
                context.update(announcements)
            SGPAquery = Semrec1.objects.get(EmailId=request.session['sUserMailId'])
            if SGPAquery.SGPA is not None:
                SGPA1={'SGPA1':SGPAquery.SGPA}
                SGPAquery = Semrec2.objects.get(EmailId=request.session['sUserMailId'])
            else:
                SGPA1={'SGPA1':0}
            if SGPAquery.SGPA is not None:
                SGPA2={'SGPA2':SGPAquery.SGPA}
                SGPAquery = Semrec3.objects.get(EmailId=request.session['sUserMailId'])
            else:
                SGPA2={'SGPA2':0}
            if SGPAquery.SGPA is not None:
                SGPA3={'SGPA3':SGPAquery.SGPA}
                SGPAquery = Semrec4.objects.get(EmailId=request.session['sUserMailId'])
            else:
                SGPA3={'SGPA3':0}
            if SGPAquery.SGPA is not None:
                SGPA4={'SGPA4':SGPAquery.SGPA}
                SGPAquery = Semrec5.objects.get(EmailId=request.session['sUserMailId'])
            else:
                SGPA4={'SGPA4':0}
            if SGPAquery.SGPA is not None:
                SGPA5={'SGPA5':SGPAquery.SGPA}
                SGPAquery = Semrec6.objects.get(EmailId=request.session['sUserMailId'])
            else:
                SGPA5={'SGPA5':0}
            if SGPAquery.SGPA is not None:
                SGPA6={'SGPA6':SGPAquery.SGPA}
                SGPAquery = Semrec7.objects.get(EmailId=request.session['sUserMailId'])
            else:
                SGPA6={'SGPA6':0}
            if SGPAquery.SGPA is not None:
                SGPA7={'SGPA7':SGPAquery.SGPA}
                SGPAquery = Semrec8.objects.get(EmailId=request.session['sUserMailId'])
            else:
                SGPA7={'SGPA7':0}
            if SGPAquery.SGPA is not None:
                SGPA8={'SGPA8':SGPAquery.SGPA}
            else:
                SGPA8={'SGPA8':0}
            context.update(SGPA1)
            context.update(SGPA2)
            context.update(SGPA3)
            context.update(SGPA4)
            context.update(SGPA5)
            context.update(SGPA6)
            context.update(SGPA7)
            context.update(SGPA8)
            return render(request, 'Home/student/dashboard.html', context)
    else:
        messages.error(request, "Invalid user credentials")
        return render(request, 'Login/Login2.html')

def sDashboard(request):
    return redirect('StudentLogin')

def sActivities(request):
    if 'sUserMailId' not in request.session:
        messages.error(request, "Session timed out")
        return redirect('Login2')
    if request.session['sUserMailId']:
        activities_done = Activities.objects.filter(EmailId=request.session['sUserMailId']).order_by('-Actdate')
        studentis = Student.objects.get(EmailId=request.session['sUserMailId'])
        actpts = studentis.Activitypts
        return render(request, 'Home/student/activities.html',{'activities':activities_done,'actpts':actpts})

def Newactivity(request):
    if request.method == 'POST':
        student = Student.objects.get(EmailId=request.session['sUserMailId'])
        newact = Activities(EmailId=request.session['sUserMailId'])
        newact.Proctor = student.Proctor
        newact.Name = student.Name
        newact.USN = student.USN
        newact.Actname = request.POST.get('activityname').capitalize()
        newact.Actdesc = request.POST.get('activitydesc').capitalize()
        newact.Actreport = request.FILES['activityreport']
        newact.Actimg = request.FILES['activityimg']
        newact.Acttype = request.POST.get('activitytype').capitalize()
        newact.Actduration = request.POST.get('actdurnum')+" "+request.POST.get('actduration')
        newact.save()
        newNot = Notifications(EmailId=request.session['sUserMailId'],
        Proctor=student.Proctor,
        Nottype="New Activity",
        Notification=student.USN)
        newNot.save()
        return redirect('sActivities')

def sRecords(request):
    if 'sUserMailId' not in request.session:
        messages.error(request, "Session timed out")
        return redirect('Login2')
    else:
        details = Student.objects.get(EmailId=request.session['sUserMailId'], Password=request.session['sUserPassword'])
        if request.method == 'POST':
            r1 = Semrec1.objects.get(EmailId=request.session['sUserMailId'])
            r2 = Semrec2.objects.get(EmailId=request.session['sUserMailId'])
            r3 = Semrec3.objects.get(EmailId=request.session['sUserMailId'])
            r4 = Semrec4.objects.get(EmailId=request.session['sUserMailId'])
            r5 = Semrec5.objects.get(EmailId=request.session['sUserMailId'])
            r6 = Semrec6.objects.get(EmailId=request.session['sUserMailId'])
            r7 = Semrec7.objects.get(EmailId=request.session['sUserMailId'])
            r8 = Semrec8.objects.get(EmailId=request.session['sUserMailId'])
            if request.POST.get('Semester1'):
                sem = details.Semester1
                if sem is None:
                    return render(request, 'Home/student/courseUpdate.html', {"sem": "1st"})
                subs = sem.split(" ")
                sem = 1
                if (r1.Course1 is not None):
                    R = [str(r1.Course1).split(), str(r1.Course2).split(), str(r1.Course3).split(), str(r1.Course4).split(), str(r1.Course5).split(),
                         str(r1.Course6).split(), str(r1.Course7).split(), str(r1.Course8).split(), str(r1.Course9).split(), str(r1.Course10).split()]
                    SGPA = format(r1.SGPA,"0.3f")
                    if (r1.Result):
                        res = r1.Result
                    else:
                        res = ""
            if request.POST.get('Semester2'):
                sem = details.Semester2
                if sem is None:
                    return render(request, 'Home/student/courseUpdate.html', {"sem": "2nd"})
                subs = sem.split(" ")
                sem = 2
                if (r2.Course1 is not None):
                    R = [str(r2.Course1).split(), str(r2.Course2).split(), str(r2.Course3).split(), str(r2.Course4).split(), str(r2.Course5).split(),
                         str(r2.Course6).split(), str(r2.Course7).split(), str(r2.Course8).split(), str(r2.Course9).split(), str(r2.Course10).split()]
                    SGPA = format(r2.SGPA,"0.3f")
                    if (r2.Result):
                        res = r2.Result
                    else:
                        res = ""
            if request.POST.get('Semester3'):
                sem = details.Semester3
                if sem is None:
                    return render(request, 'Home/student/courseUpdate.html', {"sem": "3rd"})
                subs = sem.split(" ")
                sem = 3
                if (r3.Course1 is not None):
                    R = [str(r3.Course1).split(), str(r3.Course2).split(), str(r3.Course3).split(), str(r3.Course4).split(), str(r3.Course5).split(),
                         str(r3.Course6).split(), str(r3.Course7).split(), str(r3.Course8).split(), str(r3.Course9).split(), str(r3.Course10).split()]
                    SGPA = format(r3.SGPA,"0.3f")
                    if (r3.Result):
                        res = r3.Result
                    else:
                        res = ""
            if request.POST.get('Semester4'):
                sem = details.Semester4
                if sem is None:
                    return render(request, 'Home/student/courseUpdate.html', {"sem": "4th"})
                subs = sem.split(" ")
                sem = 4
                if (r4.Course1 is not None):
                    R = [str(r4.Course1).split(), str(r4.Course2).split(), str(r4.Course3).split(), str(r4.Course4).split(), str(r4.Course5).split(),
                         str(r4.Course6).split(), str(r4.Course7).split(), str(r4.Course8).split(), str(r4.Course9).split(), str(r4.Course10).split()]
                    SGPA = format(r4.SGPA,"0.3f")
                    if (r4.Result):
                        res = r4.Result
                    else:
                        res = ""
            if request.POST.get('Semester5'):
                sem = details.Semester5
                if sem is None:
                    return render(request, 'Home/student/courseUpdate.html', {"sem": "5th"})
                subs = sem.split(" ")
                sem = 5
                if (r5.Course1 is not None):
                    R = [str(r5.Course1).split(), str(r5.Course2).split(), str(r5.Course3).split(), str(r5.Course4).split(), str(r5.Course5).split(),
                         str(r5.Course6).split(), str(r5.Course7).split(), str(r5.Course8).split(), str(r5.Course9).split(), str(r5.Course10).split()]
                    SGPA = format(r5.SGPA,"0.3f")
                    if (r5.Result):
                        res = r5.Result
                    else:
                        res = ""
            if request.POST.get('Semester6'):
                sem = details.Semester6
                if sem is None:
                    return render(request, 'Home/student/courseUpdate.html', {"sem": "6th"})
                subs = sem.split(" ")
                sem = 6
                if (r6.Course1 is not None):
                    R = [str(r6.Course1).split(), str(r6.Course2).split(), str(r6.Course3).split(), str(r6.Course4).split(), str(r6.Course5).split(),
                         str(r6.Course6).split(), str(r6.Course7).split(), str(r6.Course8).split(), str(r6.Course9).split(), str(r6.Course10).split()]
                    SGPA = format(r6.SGPA,"0.3f")
                    if (r6.Result):
                        res = r6.Result
                    else:
                        res = ""
            if request.POST.get('Semester7'):
                sem = details.Semester7
                if sem is None:
                    return render(request, 'Home/student/courseUpdate.html', {"sem": "7th"})
                subs = sem.split(" ")
                sem = 7
                if (r7.Course1 is not None):
                    R = [str(r7.Course1).split(), str(r7.Course2).split(), str(r7.Course3).split(), str(r7.Course4).split(), str(r7.Course5).split(),
                         str(r7.Course6).split(), str(r7.Course7).split(), str(r7.Course8).split(), str(r7.Course9).split(), str(r7.Course10).split()]
                    SGPA = format(r7.SGPA,"0.3f")
                    if (r7.Result):
                        res = r7.Result
                    else:
                        res = ""
            if request.POST.get('Semester8'):
                sem = details.Semester8
                if sem is None:
                    return render(request, 'Home/student/courseUpdate.html', {"sem": "8th"})
                subs = sem.split(" ")
                sem = 8
                if (r8.Course1 is not None):
                    R = [str(r8.Course1).split(), str(r8.Course2).split(), str(r8.Course3).split(), str(r8.Course4).split(), str(r8.Course5).split(),
                         str(r8.Course6).split(), str(r8.Course7).split(), str(r8.Course8).split(), str(r8.Course9).split(), str(r8.Course10).split()]
                    SGPA = format(r8.SGPA,"0.3f")
                    if (r8.Result):
                        res = r8.Result
                    else:
                        res = ""
            if request.POST.get('Supp'):
                return redirect('Supplementary') 
            if 'R' in locals():
                suppExist = Supplementary.objects.filter(EmailId=request.session['sUserMailId'],Semester=sem)
                if len(suppExist) != 0:
                    R1 = [str(suppExist[0].Course1).split(), str(suppExist[0].Course2).split(), str(suppExist[0].Course3).split(), str(suppExist[0].Course4).split(), str(suppExist[0].Course5).split(),
                         str(suppExist[0].Course6).split(), str(suppExist[0].Course7).split(), str(suppExist[0].Course8).split(), str(suppExist[0].Course9).split(), str(suppExist[0].Course10).split()]
                    SGPA1 = format(suppExist[0].SGPA,"0.3f")
                    if (suppExist[0].Result):
                        res1 = suppExist[0].Result
                    else:
                        res1 = ""
                    return render(request, 'Home/student/recordUpdate.html', {'subjects': subs, 'sem': sem, 'recs': R, 'SGPA': SGPA, 'recs1': R1, 'SGPA1': SGPA1, 'res':res, 'res1':res1})
                return render(request, 'Home/student/recordUpdate.html', {'subjects': subs, 'sem': sem, 'recs': R, 'SGPA': SGPA, 'res':res})
            else:
                return render(request, 'Home/student/recordUpdate.html', {'subjects': subs, 'sem': sem})
        return render(request, 'Home/student/records.html')

def ProctorLogin(request):
    if request.method == 'POST':
        enteremailid = request.POST.get("mailid")
        request.session['UserMailId'] = enteremailid
        enterpass = request.POST.get("password")
        request.session['UserPassword'] = enterpass
    if Proctor.objects.filter(EmailId=request.session['UserMailId'], Password=request.session['UserPassword']):
        details = Proctor.objects.get(EmailId=request.session['UserMailId'])
        context = {"mailid": request.session['UserMailId']}
        if details.Name:
            allannouncements = Announcements.objects.filter(AnnouncedBy=details.Name).order_by('-id')
            announcements = {"announcement": allannouncements}
            context.update(announcements)
            Name = {"Name": details.Name.title()}
            context.update(Name)
        else:
            context.update()
        if details.Department:
            Department = {"Department": details.Department.upper()}
            context.update(Department)
        else:
            context.update()
        if details.ProctorId:
            ProctorId = {"ProctorId": details.ProctorId.upper()}
            context.update(ProctorId)
        else:
            context.update()
        if details.Profilepic:
            Profilepic = {"Profilepic": details.Profilepic}
            context.update(Profilepic)
        else:
            context.update()
        proctor = Proctor.objects.get(EmailId=request.session['UserMailId'])
        NoofStudents = Student.objects.filter(Proctor=proctor.Name,Archived="no").order_by('USN')
        request.session['NoofStudents'] = len(NoofStudents)
        x = 0
        Y1 = 0
        Y2 = 0
        Y3 = 0
        Y4 = 0
        #find 4th years
        for i in range(0,len(NoofStudents)):
            if int(NoofStudents[i].USN[3:5]) > x:
                x = int(NoofStudents[i].USN[3:5])
        #differentiate into diff years
        for j in range(0,len(NoofStudents)):
            if int(NoofStudents[j].USN[3:5]) == x:
                Y4 += 1
            elif int(NoofStudents[j].USN[3:5]) == x-1:
                Y3 += 1
            elif int(NoofStudents[j].USN[3:5]) == x-2:
                Y2 += 1
            else:
                Y1 += 1
        archived = Student.objects.filter(Proctor=proctor.Name,Archived="yes")
        A = len(archived)
        NoofStudents = {"NoofStudents": request.session['NoofStudents'],"Y1":Y1,"Y2":Y2,"Y3":Y3,"Y4":Y4,"A":A,"x":(2000+x)}
        context.update(NoofStudents)
        return render(request, 'Home/proctor/dashboard.html', context)
    else:
        messages.error(request, "Invalid user credentials")
        return render(request, 'Login/Login3.html')

def Announce(request):
    if request.method == 'POST':
        announceHead = request.POST.get('announceHead')
        announceDesc = request.POST.get('announceDesc')
        if request.POST.get('announceLink') is not None:
            announceLink = request.POST.get('announceLink')
        else:
            announceLink = ""
        details = Proctor.objects.get(EmailId=request.session['UserMailId'])
        NewAnnouncement = Announcements(
            details.Name, announceHead.capitalize(), announceDesc.capitalize(), announceLink)
        NewAnnouncement.save()
    return redirect('ProctorLogin')

def pDashboard(request):
    return redirect('ProctorLogin')

def pStudentlist(request):
    if 'UserMailId' not in request.session:
        messages.error(request, "Session timed out")
        return redirect('Login3')
    if request.session['UserMailId']:
        proctor = Proctor.objects.get(EmailId=request.session['UserMailId'])
        all_students = Student.objects.filter(Proctor=proctor.Name,Semester=9)
        all_students.update(Archived="yes")
        details = Student.objects.filter(Proctor=proctor.Name,Archived="no").order_by('USN')
        x = 0
        Y1 = []
        Y2 = []
        Y3 = []
        Y4 = []
        #find 4th years
        for i in range(0,len(details)):
            if int(details[i].USN[3:5]) > x:
                x = int(details[i].USN[3:5])
        #differentiate into diff years
        for j in range(0,len(details)):
            if int(details[j].USN[3:5]) == x:
                Y4.append(details[j])
            elif int(details[j].USN[3:5]) == x-1:
                Y3.append(details[j])
            elif int(details[j].USN[3:5]) == x-2:
                Y2.append(details[j])
            else:
                Y1.append(details[j])
        context = {"Y1":Y1,"Y2":Y2,"Y3":Y3,"Y4":Y4}
        return render(request, 'Home/proctor/studentlist.html', context)

def Manage(request):
    if 'UserMailId' not in request.session:
        messages.error(request, "Session timed out")
        return redirect('Login3')
    proctor = Proctor.objects.get(EmailId=request.session['UserMailId'])
    context = {
        'notifications':Notifications.objects.filter(Proctor=proctor.Name).order_by('-Date'),
        'NoofNots':len(Notifications.objects.filter(Proctor=proctor.Name)),
        'archived':Student.objects.filter(Proctor=proctor.Name,Archived="yes").order_by('USN'),
        'NoofArchived':len(Student.objects.filter(Proctor=proctor.Name,Archived="yes")),
        'TotalStudents':request.session['NoofStudents'] + len(Student.objects.filter(Proctor=proctor.Name,Archived="yes")),
        'students':Student.objects.filter(Proctor=proctor.Name,Archived="no").order_by('Name'),
        'activities':Activities.objects.filter(Proctor=proctor.Name,Actpts=0,Reject="N").order_by('USN'),
    }
    if request.method == 'POST':
        if request.POST.get('0'):
            return render(request, 'Home/proctor/updateForm.html',context)
        elif request.POST.get('1'):
            return render(request, 'Home/proctor/viewActivity.html',context)
        elif request.POST.get('2'):
            return render(request, 'Home/proctor/viewArchive.html',context)
        elif request.POST.get('3'):
            return render(request, 'Home/proctor/manage.html',context)
        else:
            recipients = ""
            reciveList = []
            for i in range(1,request.session['NoofStudents']+1):
                if request.POST.get(f'input{i}'):
                    recipients=recipients + (request.POST.get(f'input{i}')) + " "
                    reciveList.append((request.POST.get(f'input{i}')))
            updateList = ""
            for i in range(-6,0):
                if request.POST.get(f'input{i}'):
                    updateList=updateList + (request.POST.get(f'input{i}')) + " "
            print(updateList)
            notnoti = Notifications(Proctor=f"{proctor.Name}Forms",
            EmailId="sourabh.is20@bmsce.ac.in",
            Nottype=updateList,
            Notification=recipients)
            notnoti.save()
            send_mail(
                'Record Update',
                'Please click on the link below to update your info\
                \nhttp://127.0.0.1:8000/Recordupdateform',
                settings.EMAIL_HOST_USER,
                reciveList,
                fail_silently=True
            )
            messages.success(request, "Updateform mailed successfully")
            return render(request, 'Home/proctor/manage.html',context)
    return render(request, 'Home/proctor/manage.html',context)

def Kickstudent(request):
    if request.method == 'POST':
        kick = Student.objects.get(USN=request.POST.get('USN'))
        kick.delete()
        messages.success(request, f"{kick.Name} has been kicked out")
        return redirect('pStudentlist')

def ViewStudent(request):
    if request.method == 'POST':
        sUSN = request.POST.get('sUSN')
        sdetails = Student.objects.get(USN=sUSN)
        request.session['sUserMailId'] = sdetails.EmailId
        request.session['sUserPassword'] = sdetails.Password
    return redirect('StudentLogin')

def CoordinatorLogin(request):
    if request.method == 'POST':
        enteremailid = request.POST.get("mailid")
        enterpass = request.POST.get("password")
    if Coordinator.objects.filter(EmailId=enteremailid, Password=enterpass):
        return render(request, 'Home/coordinator/dashboard.html')
    else:
        messages.error(request, "Invalid user credentials")
        return render(request, 'Login/Login4.html')

def updateSDb(request):
    if request.method == 'POST':
        queryobj = Student.objects.get(EmailId=request.session['sUserMailId'])
        if request.POST.get('Name'):
            queryobj.Name = request.POST.get('Name').capitalize()
            queryobj.save()
        if request.POST.get('USN'):
            queryobj.USN = request.POST.get('USN').upper()
            queryobj.save()
            a = Semrec1(USN=request.POST.get('USN').upper())
            b = Semrec2(USN=request.POST.get('USN').upper())
            c = Semrec3(USN=request.POST.get('USN').upper())
            d = Semrec4(USN=request.POST.get('USN').upper())
            e = Semrec5(USN=request.POST.get('USN').upper())
            f = Semrec6(USN=request.POST.get('USN').upper())
            g = Semrec7(USN=request.POST.get('USN').upper())
            h = Semrec8(USN=request.POST.get('USN').upper())
            a.save()
            b.save()
            c.save()
            d.save()
            e.save()
            f.save()
            g.save()
            h.save()
        if request.POST.get('Pname'):
            queryobj.Proctor = request.POST.get('Pname').lower()
            queryobj.save()
        if request.POST.get('Branch'):
            queryobj.Branch = request.POST.get('Branch').upper()
            queryobj.save()
        if request.POST.get('Semester'):
            queryobj.Semester = request.POST.get('Semester')
            queryobj.save()
        if request.POST.get('Section'):
            queryobj.Section = request.POST.get('Section').upper()
            queryobj.save()

    return redirect('StudentLogin')

def updatePDb(request):
    if request.method == 'POST':
        queryobj = Proctor.objects.get(EmailId=request.session['UserMailId'])
        if request.POST.get('Name'):
            queryobj.Name = request.POST.get('Name').lower()
            queryobj.save()
        if request.POST.get('ProctorId'):
            queryobj.ProctorId = request.POST.get('ProctorId').lower()
            queryobj.save()

    return redirect('ProctorLogin')

def updateCDb(request):
    if request.method == 'POST':
        queryobj = Student.objects.get(EmailId=request.session['sUserMailId'])
        for i in range(1, 9):
            if i == 1:
                for j in range(1, 11):
                    if request.POST.get(f'{i}stcourse{j}'):
                        temp = queryobj.Semester1
                        if temp is None:
                            data = request.POST.get(f'{i}stcourse{j}').upper()
                        else:
                            data = str(temp) + " " + request.POST.get(f'{i}stcourse{j}').upper()
                        queryobj.Semester1 = data
                        queryobj.save()
            if i == 2:
                for j in range(1, 11):
                    if request.POST.get(f'{i}ndcourse{j}'):
                        temp = queryobj.Semester2
                        if temp is None:
                            data = request.POST.get(f'{i}ndcourse{j}').upper()
                        else:
                            data = str(temp) + " " + request.POST.get(f'{i}ndcourse{j}').upper()
                        queryobj.Semester2 = data
                        queryobj.save()
            if i == 3:
                for j in range(1, 11):
                    if request.POST.get(f'{i}rdcourse{j}'):
                        temp = queryobj.Semester3
                        if temp is None:
                            data = request.POST.get(f'{i}rdcourse{j}').upper()
                        else:
                            data = str(temp) + " " + request.POST.get(f'{i}rdcourse{j}').upper()
                        queryobj.Semester3 = data
                        queryobj.save()
            if i == 4:
                for j in range(1, 11):
                    if request.POST.get(f'{i}thcourse{j}'):
                        temp = queryobj.Semester4
                        if temp is None:
                            data = request.POST.get(f'{i}thcourse{j}').upper()
                        else:
                            data = str(temp) + " " + request.POST.get(f'{i}thcourse{j}').upper()
                        print(data)
                        queryobj.Semester4 = data
                        queryobj.save()
            if i == 5:
                for j in range(1, 11):
                    if request.POST.get(f'{i}thcourse{j}'):
                        temp = queryobj.Semester5
                        if temp is None:
                            data = request.POST.get(f'{i}thcourse{j}').upper()
                        else:
                            data = str(temp) + " " + request.POST.get(f'{i}thcourse{j}').upper()
                        queryobj.Semester5 = data
                        queryobj.save()
            if i == 6:
                for j in range(1, 11):
                    if request.POST.get(f'{i}thcourse{j}'):
                        temp = queryobj.Semester6
                        if temp is None:
                            data = request.POST.get(f'{i}thcourse{j}').upper()
                        else:
                            data = str(temp) + " " + request.POST.get(f'{i}thcourse{j}').upper()
                        queryobj.Semester6 = data
                        queryobj.save()
            if i == 7:
                for j in range(1, 11):
                    if request.POST.get(f'{i}thcourse{j}'):
                        temp = queryobj.Semester7
                        if temp is None:
                            data = request.POST.get(f'{i}thcourse{j}').upper()
                        else:
                            data = str(temp) + " " + request.POST.get(f'{i}thcourse{j}').upper()
                        queryobj.Semester7 = data
                        queryobj.save()
            if i == 8:
                for j in range(1, 11):
                    if request.POST.get(f'{i}thcourse{j}'):
                        temp = queryobj.Semester8
                        if temp is None:
                            data = request.POST.get(f'{i}thcourse{j}').upper()
                        else:
                            data = str(temp) + " " + request.POST.get(f'{i}thcourse{j}').upper()
                        queryobj.Semester8 = data
                        queryobj.save()
    messages.success(request, "Courses updated successfully")
    return redirect('sRecords')

def updateRDb(request):
    if request.method == 'POST':
        if (int(request.POST.get('sem')) == 1):
            print("1")
            queryobj1 = Semrec1.objects.get(EmailId=request.session['sUserMailId'])
        elif (int(request.POST.get('sem')) == 2):
            print("2")
            queryobj1 = Semrec2.objects.get(EmailId=request.session['sUserMailId'])
        elif (int(request.POST.get('sem')) == 3):
            print("3")
            queryobj1 = Semrec3.objects.get(EmailId=request.session['sUserMailId'])
        elif (int(request.POST.get('sem')) == 4):
            print("4")
            queryobj1 = Semrec4.objects.get(EmailId=request.session['sUserMailId'])
        elif (int(request.POST.get('sem')) == 5):
            print("5")
            queryobj1 = Semrec5.objects.get(EmailId=request.session['sUserMailId'])
        elif (int(request.POST.get('sem')) == 6):
            print("6")
            queryobj1 = Semrec6.objects.get(EmailId=request.session['sUserMailId'])
        elif (int(request.POST.get('sem')) == 7):
            print("7")
            queryobj1 = Semrec7.objects.get(EmailId=request.session['sUserMailId'])
        else:
            print("8")
            queryobj1 = Semrec8.objects.get(EmailId=request.session['sUserMailId'])

        updateRec(request,queryobj1)
        
        student = Student.objects.get(EmailId=request.session['sUserMailId'])
        newNot = Notifications(EmailId=request.session['sUserMailId'],
        Proctor=student.Proctor,
        Nottype="Record update",
        Notification=student.USN)
        newNot.save()
        messages.success(request, "Record updated successfully")
        return redirect('sRecords')

def updatePP(request):
    if request.method == 'POST':
        if 'sprofilepic' in request.FILES:
            profile = Student.objects.get(EmailId=request.session['sUserMailId'])
            profile.Profilepic = request.FILES['sprofilepic']
            profile.save()
            return redirect('StudentLogin')
        if 'pprofilepic' in request.FILES:
            profile = Proctor.objects.get(EmailId=request.session['UserMailId'])
            profile.Profilepic = request.FILES['pprofilepic']
            profile.save()
            return redirect('ProctorLogin')

def sLogout(request):
    if 'sUserMailId' not in request.session:
        return redirect('Login1')
    else:
        del request.session['sUserMailId']
        del request.session['sUserPassword']
        return redirect('Login1')

def pLogout(request):
    proctor = Proctor.objects.get(EmailId=request.session['UserMailId'])
    notifications = Notifications.objects.filter(Proctor=proctor.Name)
    notifications.delete()
    if 'UserMailId' not in request.session:
        return redirect('Login1')
    else:
        del request.session['UserMailId']
        del request.session['UserPassword']
        del request.session['NoofStudents']
        return redirect('Login1')

def Recordupdateform(request):
    if 'sUserMailId' in request.session:
        temp = Student.objects.get(EmailId=request.session['sUserMailId'])
        form = Notifications.objects.filter(Proctor=(f'{temp.Proctor}Forms'),Date__year=date.today().year,Date__month=date.today().month,Date__day=date.today().day)
        if form:
            for i in form:
                if request.session['sUserMailId'] in i.Notification:
                    print("yes")
                    updateList = i.Nottype.split(" ")
                    for j in updateList:
                        if j == "":
                            updateList.remove(j)
                    break
            return render(request, 'recordupdateform.html',{'list':updateList})
        return HttpResponse('<a href="sLogout">form not available</a>')
    else:
        if request.method == 'POST':
            enteremailid = request.POST.get("mailid")
            request.session['sUserMailId'] = enteremailid
            enterpass = request.POST.get("password")
            request.session['sUserPassword'] = enterpass
            if Student.objects.filter(EmailId=request.session['sUserMailId'], Password=request.session['sUserPassword']):
                return redirect('Recordupdateform')
            else:
                del request.session['sUserMailId']
                del request.session['sUserPassword']
                messages.warning(request,'Invalid Credentials')
        return render(request, 'recordupdateform.html')

def ViewActivity(request):
    activity = Activities.objects.filter(USN=request.POST.get('USN'),Actname=request.POST.get('Actname'),Actpts=0,Reject="N")
    student = Student.objects.get(USN=request.POST.get('USN'))
    context = {
        'activity':activity[0]
    }
    print(context)
    if request.POST.get('points'):
        context['activity'].Actpts = int(request.POST.get('points'))
        student.Activitypts = student.Activitypts + int(request.POST.get('points'))
        context['activity'].save()
        student.save()
        return redirect('Manage')
    return render(request, 'Home/proctor/stuActivity.html',context)

def forgotPass(request):
    secCode = ""
    if request.method == 'POST':
        if request.POST.get('forgotPass1'):
            request.session['MailId'] = request.POST.get('EmailId')
            details = list(chain(Student.objects.filter(EmailId = request.session['MailId']),Proctor.objects.filter(EmailId = request.session['MailId'])))
            if details == []:
                messages.error(request, "Sorry, No such account exists")
                return render(request, 'forgotPass.html')
            for i in range(0,3):
                secCode += random.choice(string.ascii_letters) + random.choice(string.digits)
            request.session['secCode'] = secCode
            send_mail(
                'Password change confirmation',
                f'A password change request has been made by your account\
                \nIgnore the mail and do not share the code if not requested by you.\
                \nSecret code to change the password:-\
                \n{secCode}',
                settings.EMAIL_HOST_USER,
                [request.session['MailId']],
                fail_silently=True
            )
            print(secCode)
            return render(request, 'forgotPass.html', {'email':request.session['MailId']})    
        if request.POST.get('secCode') == request.session['secCode']:
            details = list(chain(Student.objects.filter(EmailId = request.session['MailId']),Proctor.objects.filter(EmailId = request.session['MailId'])))
            details[0].Password = request.POST.get('NewPass')
            details[0].save()
            messages.success(request, "Password updated successfully")
            return render(request, 'forgotPass.html', {'secCode':request.POST.get('secCode')})
        else:
            messages.error(request, "Something went wrong!!!Please try again")
            return render(request, 'forgotPass.html')
    else:
        return render(request, 'forgotPass.html')

def supplementary(request):
    if 'sUserMailId' not in request.session:
        messages.error(request, "Session timed out")
        return redirect('Login2')
    else:
        checkDB = Supplementary.objects.filter(EmailId=request.session['sUserMailId'],Course1="")
        if len(checkDB) != 0:
            a = checkDB[0].Courses.split(" ")
            return render(request, 'Home/student/supprecordUpdate.html',{'a':a,'sem':checkDB[0].Semester})
        details = Student.objects.get(EmailId=request.session['sUserMailId'], Password=request.session['sUserPassword'])
        if request.POST.get('Semester'):
            checkDB = Supplementary.objects.filter(EmailId=request.session['sUserMailId'],Semester=request.POST.get('Semester'))
            if checkDB is not None:
                messages.error(request, "Record cannot be updated")
                return redirect('sRecords')
            newSupp = Supplementary(USN=details.USN,Name=details.Name,EmailId=request.session['sUserMailId'])
            newSupp.Semester = request.POST.get('Semester')
            for j in range(1, 11):
                    if request.POST.get(f'0course{j}'):
                        temp = newSupp.Courses
                        if temp is None:
                            data = request.POST.get(f'0course{j}').upper()
                            a = [request.POST.get(f'0course{j}').upper()]
                        else:
                            data = str(temp) + " " + request.POST.get(f'0course{j}').upper()
                            a.append(request.POST.get(f'0course{j}').upper())
                        newSupp.Courses = data
                        newSupp.save()
            
            return render(request, 'Home/student/supprecordUpdate.html',{'a':a,'sem':newSupp.Semester})

        return render(request, 'Home/student/courseUpdate.html', {"sem":"0"})

def updateSuppDb(request):
    if request.POST.get('sem'):
        queryobj1 = Supplementary.objects.get(EmailId=request.session['sUserMailId'],Semester=request.POST.get('sem'))
        updateRec(request,queryobj1)

        student = Student.objects.get(EmailId=request.session['sUserMailId'])
        newNot = Notifications(EmailId=request.session['sUserMailId'],
        Proctor=student.Proctor,
        Nottype="Supplementary record",
        Notification=student.USN)
        newNot.save()
        messages.success(request, "Record updated successfully")
        return redirect('sRecords')

def updateRec(request,queryobj1):
    # course1
    for j in range(1, 10):
        if request.POST.get(f'1input{j}'):
            temp = queryobj1.Course1
            if j == 1:
                data = request.POST.get('1course') + " " + str(request.POST.get(f'1input{j}'))
            else:
                data = str(temp) + " " + str(request.POST.get(f'1input{j}'))
            queryobj1.Course1 = data.upper()
            queryobj1.save()
    # course2
    for j in range(1, 10):
        if request.POST.get(f'2input{j}'):
            temp = queryobj1.Course2
            if j == 1:
                data = str(request.POST.get('2course')) + " " + request.POST.get(f'2input{j}')
            else:
                data = str(temp) + " " + str(request.POST.get(f'2input{j}'))
            queryobj1.Course2 = data.upper()
            queryobj1.save()
    # course3
    for j in range(1, 10):
        if request.POST.get(f'3input{j}'):
            temp = queryobj1.Course3
            if j == 1:
                data = str(request.POST.get('3course')) + " " + str(request.POST.get(f'3input{j}'))
            else:
                data = str(temp) + " " + str(request.POST.get(f'3input{j}'))
            queryobj1.Course3 = data.upper()
            queryobj1.save()
    # course4
    for j in range(1, 10):
        if request.POST.get(f'4input{j}'):
            temp = queryobj1.Course4
            if j == 1:
                data = str(request.POST.get('4course')) + " " + str(request.POST.get(f'4input{j}'))
            else:
                data = str(temp) + " " + str(request.POST.get(f'4input{j}'))
            queryobj1.Course4 = data.upper()
            queryobj1.save()
    # course5
    for j in range(1, 10):
        if request.POST.get(f'5input{j}'):
            temp = queryobj1.Course5
            if j == 1:
                data = str(request.POST.get('5course')) + " " + str(request.POST.get(f'5input{j}'))
            else:
                data = str(temp) + " " + str(request.POST.get(f'5input{j}'))
            queryobj1.Course5 = data.upper()
            queryobj1.save()
    # course6
    for j in range(1, 10):
        if request.POST.get(f'6input{j}'):
            temp = queryobj1.Course6
            if j == 1:
                data = str(request.POST.get('6course')) + " " + str(request.POST.get(f'6input{j}'))
            else:
                data = str(temp) + " " + str(request.POST.get(f'6input{j}'))
            queryobj1.Course6 = data.upper()
            queryobj1.save()
    # course7
    for j in range(1, 10):
        if request.POST.get(f'7input{j}'):
            temp = queryobj1.Course7
            if j == 1:
                data = str(request.POST.get('7course')) + " " + str(request.POST.get(f'7input{j}'))
            else:
                data = str(temp) + " " + str(request.POST.get(f'7input{j}'))
            queryobj1.Course7 = data.upper()
            queryobj1.save()
    # course8
    for j in range(1, 10):
        if request.POST.get(f'8input{j}'):
            temp = queryobj1.Course8
            if j == 1:
                data = str(request.POST.get('8course')) + " " + str(request.POST.get(f'8input{j}'))
            else:
                data = str(temp) + " " + str(request.POST.get(f'8input{j}'))
            queryobj1.Course8 = data.upper()
            queryobj1.save()
    # course9
    for j in range(1, 10):
        if request.POST.get(f'9input{j}'):
            temp = queryobj1.Course9
            if j == 1:
                data = str(request.POST.get('9course')) + " " + str(request.POST.get(f'9input{j}'))
            else:
                data = str(temp) + " " + str(request.POST.get(f'9input{j}'))
            queryobj1.Course9 = data.upper()
            queryobj1.save()
    # course10
    for j in range(1, 10):
        if request.POST.get(f'10input{j}'):
            temp = queryobj1.Course10
            if j == 1:
                data = str(request.POST.get('10course')) + " " + str(request.POST.get(f'10input{j}'))
            else:
                data = str(temp) + " " + str(request.POST.get(f'10input{j}'))
            queryobj1.Course10 = data.upper()
            queryobj1.save()
    #SGPA
    N = 0
    D = 0
    for i in range(1,10):
        if (request.POST.get(f'{i}input1') and request.POST.get(f'{i}input9')):
            N = N + int(request.POST.get(f'{i}input1'))*int(request.POST.get(f'{i}input9'))
            D = D + int(request.POST.get(f'{i}input1'))
        else:
            SGPA = N/D
            queryobj1.SGPA = SGPA
            queryobj1.save()
            break
    
def rejectAct(request):
    if request.method == 'POST':
        Act = Activities.objects.filter(USN=request.POST.get('USN'),
                                    Actname=request.POST.get('Actname'),
                                    Actpts=0)
        if len(Act)>0:
            temp = Act[0]
            temp.Reject = "Y"
            temp.save()
    return redirect('Manage')

def Help(request):
    return redirect('About')

def About(request):
    return render(request, 'Home/help/about.html')

def Report(request):
    return render(request, 'Home/help/report.html')

def Tutorial(request):
    return render(request, 'Home/help/tutorial.html')

def Reportform(request):
    if request.method == 'POST':
        if request.POST.get('Name'):
            print("form1")
        elif request.POST.get('USN'):
            print("form2")
    return redirect('Report')

def UploadRes(request):
    if request.method == 'POST':
        if 'result' in request.FILES:
            record = switch(request,request.POST.get('sem'))
            record.Result = request.FILES['result']
            record.save()
    return redirect('sRecords')

def switch(request,sem):
    switcher = {
        '1': Semrec1.objects.get(EmailId=request.session['sUserMailId']),
        '2': Semrec2.objects.get(EmailId=request.session['sUserMailId']),
        '3': Semrec3.objects.get(EmailId=request.session['sUserMailId']),
        '4': Semrec4.objects.get(EmailId=request.session['sUserMailId']),
        '5': Semrec5.objects.get(EmailId=request.session['sUserMailId']),
        '6': Semrec6.objects.get(EmailId=request.session['sUserMailId']),
        '7': Semrec7.objects.get(EmailId=request.session['sUserMailId']),
        '8': Semrec8.objects.get(EmailId=request.session['sUserMailId']),
    }
    return switcher.get(sem)