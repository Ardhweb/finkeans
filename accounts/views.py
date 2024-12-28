from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
User = get_user_model()

from django.shortcuts import render
from django.http import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout                                         
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import AnonymousUser
from django.http.response import HttpResponseRedirect
from django.template.context import RequestContext
from django.urls import reverse


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
                    return redirect('club:dashboard')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    logout(request)
    return HttpResponseRedirect(request,'log_out.html',context_instance = RequestContext(request))
    



def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid ():
            new_user = user_form.save(commit=False)

            new_user.set_password(
                                user_form.cleaned_data['password'])

            new_user.save()

            return render(request,'accounts/register_done.html',{'new_user': new_user})
    else:
        user_form = RegistrationForm()
    return render(request,'accounts/register.html',{'user_form': user_form})
            

#signup for new customers that don't have account
def signup(request):
    return render(request, 'accounts/signup.html')





#Password
