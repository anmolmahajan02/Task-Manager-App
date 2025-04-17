from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.
class task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    discription = models.TextField(max_length=5000)
    lastDate = models.DateField(default=datetime.now)
    createdAt = models.DateField(auto_now_add=True)
    email = models.EmailField(default="none@gmail.com")

