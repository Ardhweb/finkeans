from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
User = get_user_model()

from django.shortcuts import render
from django.http import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login                                         
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import AnonymousUser
from django.http.response import HttpResponseRedirect
from django.template.context import RequestContext
from django.urls import reverse
from django.contrib.auth import logout as auth_logout



def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid ():
            new_user = user_form.save(commit=False)

            new_user.set_password(
                                user_form.cleaned_data['password'])

            new_user.save()

            return redirect('accounts:account_login')
    else:
        user_form = RegistrationForm()
    return render(request,'accounts/register.html',{'user_form': user_form})
            

def logout(request):
    auth_logout(request) 
    return redirect("index")
    


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                        username=cd['username'],
                                        password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('club:club_dashboard')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})





#Password
