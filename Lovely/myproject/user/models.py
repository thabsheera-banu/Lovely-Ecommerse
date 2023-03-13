from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserOTP(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	time_st = models.DateTimeField(auto_now = True)
	otp = models.IntegerField()

# class UserDetail(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
#     mobile=models.CharField(max_length=10,null=True)

