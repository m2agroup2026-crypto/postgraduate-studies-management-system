from django.db import models
class Department(models.Model):
    code=models.CharField(max_length=20,unique=True)
    name_ar=models.CharField(max_length=150)
    name_en=models.CharField(max_length=150,blank=True)
    def __str__(self): return self.name_ar
class AcademicDegree(models.Model):
    code=models.CharField(max_length=20,unique=True)
    name_ar=models.CharField(max_length=100)
    def __str__(self): return self.name_ar
