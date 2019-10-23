from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm, CustomUserCreationForm


# Create your views here.
def signup(request):
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')

    else:  # == 'GET'
        form = CustomUserCreationForm()
    context = {'form': form, }
    return render(request, 'accounts/form.html', context)


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
    return render(request, 'accounts/form.html', context)



def logout(request):
    auth_logout(request)
    return redirect('articles:index')


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('articles:index')


@login_required
def update(request):
    if request.method == 'POST':
        #수정해주세요 요청이 들어올 때
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')

    else:  # ==> GET 요청이 들어올 때
        # 수정할 수 있는 페이지 주세요 요청이 들어올 때
        form = CustomUserChangeForm(instance=request.user)

    context = {'form': form}
    return render(request, 'accounts/form.html', context)


@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:update')
    else:
        form = PasswordChangeForm(request.user)
        context = {'form': form}
        return render(request, 'accounts/form.html', context)
