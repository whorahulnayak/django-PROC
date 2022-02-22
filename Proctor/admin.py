from django.contrib import admin
from .models import (Bugs, Notifications, Requests, Student, 
Proctor, Coordinator, Announcements, Semrec1, Semrec2, Semrec3, 
Semrec4, Semrec5, Semrec6, Semrec7, Semrec8, Activities, Supplementary)
# Register your models here.

admin.site.register(Student)
admin.site.register(Proctor)
admin.site.register(Coordinator)
admin.site.register(Announcements)
admin.site.register(Semrec1)
admin.site.register(Semrec2)
admin.site.register(Semrec3)
admin.site.register(Semrec4)
admin.site.register(Semrec5)
admin.site.register(Semrec6)
admin.site.register(Semrec7)
admin.site.register(Semrec8)
admin.site.register(Activities)
admin.site.register(Notifications)
admin.site.register(Supplementary)
admin.site.register(Bugs)
admin.site.register(Requests)
