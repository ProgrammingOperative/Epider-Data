from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Report(models.Model):
    sample_id = models.CharField(max_length=100)
    prediction = models.TextField()
    probability = models.FloatField()
    date  = models.DateTimeField(default=timezone.now)
    urgency = models.TextField()
    organization = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.sample_id
