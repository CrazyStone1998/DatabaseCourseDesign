# coding=utf-8
from django import forms


class loginForm(forms.Form):

    user_id = forms.CharField(label='Your name',max_length=20)
    passwd = forms.PasswordInput()