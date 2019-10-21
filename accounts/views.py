from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST


# Create your views here.
def signup(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')

    else:  # == 'GET'
        form = UserCreationForm()
    context = {'form': form, }
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)  # 시험 문제: AuthenticationForm 에만 request가 들어간다.
        if form.is_valid():
            auth_login(request, form.get_user())
            next_page = request.GET.get('next')  # url 에 있는 변수 꺼내기
            return redirect(next_page or 'articles:index')

    else:  # == 'GET'
        form = AuthenticationForm()
        
    context = {'form': form}
    return render(request, 'accounts/login.html', context)



def logout(request):
    auth_logout(request)
    return redirect('articles:index')


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('articles:index')