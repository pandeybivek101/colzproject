from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

	def clean_first_name(self):
		first_name = self.cleaned_data['first_name']
		if not first_name.isalpha():
			raise forms.ValidationError("Name cannot be digit")
		else:
			return first_name.title()

	def clean_last_name(self):
		last_name = self.cleaned_data['last_name']
		if not last_name.isalpha():
			raise forms.ValidationError("Name cannot be digit")
		return last_name.title()

	def clean_email(self):
		email = self.cleaned_data['email']
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("Email already exists")
		else:
			return email

