from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages

# Create your views here.

"""Registering the user"""
def RegisterUser(request):
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			messages.success(request, f'Account creation Successful')
			#return redirect('loginuser',{'title':"GO Travellers | Login"})
			return redirect("loginuser")
	else:
		form = UserRegistrationForm()
	#return render(request, "signupuser.html", {"form":form,'title':"GO Travellers | Registration"})
	return render(request, "signupuser.html", {"form":form})

#used auth_views to login

"""Logging out the user """   
@login_required
def LogoutUser(request):
    logout(request)      
    return redirect("HomePage")




