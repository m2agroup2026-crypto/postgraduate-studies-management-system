from django.db import models
from apps.theses.models import Thesis
class DefenseCommittee(models.Model):
    thesis=models.OneToOneField(Thesis,on_delete=models.PROTECT)
    defense_date=models.DateField(null=True,blank=True)
    status=models.CharField(max_length=50,default='SCHEDULED')
