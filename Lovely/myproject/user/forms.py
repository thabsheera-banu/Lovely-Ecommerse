from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import UserDetail

class SignUpForm(UserCreationForm):
    name=forms.CharField(label=("Full Name"))
    username=forms.EmailField(label=("Email"))
    class Meta:
        model=User
        fields=('name','username','password1','password2')


    
# class UserUpdate(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','email','username']

# class profileUpdate(forms.ModelForm):
#     class Meta:
#         model=UserDetail
#         fields=['mobile']