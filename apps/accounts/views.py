# apps/accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, EditProfileForm
from .models import User


def register(request):
    """ثبت‌نام کاربر"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()

                # ذخیره در SQL Server
                sql_result = user.save_to_sql()
                if sql_result:
                    messages.success(request, 'Registration successful! Data saved to SQL Server.')
                else:
                    messages.warning(request, 'Registration successful but SQL Server save failed.')

                login(request, user)
                return redirect('core:home')
            except Exception as e:
                print(f"❌ خطا در ثبت‌نام: {e}")
                messages.error(request, f'Registration error: {str(e)}')
        else:
            print("❌ فرم معتبر نیست:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """ورود کاربر"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('core:home')
            else:
                messages.error(request, 'Invalid username or password!')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    """خروج کاربر"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('core:home')


@login_required
def profile(request):
    """نمایش پروفایل کاربر"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    """ویرایش پروفایل کاربر"""
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # اگر رمز عبور تغییر کرده
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data['password'])

            user.save()

            # به‌روزرسانی در SQL Server
            user.update_in_sql()

            # اگر رمز عبور تغییر کرده، سشن را به‌روزرسانی کن
            if form.cleaned_data.get('password'):
                update_session_auth_hash(request, user)

            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})