from django.db import models
from apps.academics.models import Department
class Student(models.Model):
    university_id=models.CharField(max_length=50,unique=True)
    name_ar=models.CharField(max_length=200)
    national_id=models.CharField(max_length=14,blank=True)
    department=models.ForeignKey(Department,on_delete=models.PROTECT)
    def __str__(self): return self.name_ar
