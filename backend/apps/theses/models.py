from django.db import models
from apps.students.models import Student
class Thesis(models.Model):
    student=models.OneToOneField(Student,on_delete=models.PROTECT)
    title_ar=models.TextField()
    status=models.CharField(max_length=50,default='REGISTERED')
