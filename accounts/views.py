from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')

    else:  # == 'GET'
        form = UserCreationForm()
    context = {'form': form, }
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)  # 시험 문제: AuthenticationForm 에만 request가 들어간다.
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')

    else:  # == 'GET'
        form = AuthenticationForm()
        
    context = {'form': form}
    return render(request, 'accounts/login.html', context)



def logout(request):
    auth_logout(request)
    return redirect('articles:index')