from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login


@login_required(login_url='login/')
def profile(request):
    return render(request, 'profile.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect('profile/')

    token = {}
    token.update(csrf(request))
    token['form'] = UserRegistrationForm()

    return render(request, 'register.html', token)
