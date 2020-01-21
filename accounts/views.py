from django.shortcuts import render,redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from accounts.forms import UserLoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout,
	)
from .forms import UserLoginForm,MyRegistrationForm,PasswordResetForm

def site(request):
	if request.method =='POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username=username,password=password)
			login(request, user)
			if user.groups.filter(name='Service Provider').exists():
				return HttpResponseRedirect('/dashboard/worker/')
			if user.is_staff==True:
				return HttpResponseRedirect('/admin/')
		else:
			return render(request, 'accounts/login1.html',{"form":form})
	else:
		form = UserLoginForm()
		args = {'form':form}
		args.update(csrf(request))
		args['form'] = UserLoginForm()
		return render(request,'accounts/login1.html',args)

@csrf_protect
def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

@csrf_protect
@ensure_csrf_cookie
def register_view(request):
	if request.method =='POST':
		form = MyRegistrationForm(request.POST)  
		if form.is_valid():
			user = (form.save(commit=False))
			p = form.cleaned_data['phone']
			user = form.save()
			user.refresh_from_db()
			user.profile.phone = p
			user.is_active = True
			user.save()
			group = form.cleaned_data.get('group')
			user.groups.add(group)
			return redirect('/success/')
			return HttpResponse('Please confirm your email address to complete the registration')
		else:
			return render(request,'accounts/register.html',{"form":form})

	else:
		form = MyRegistrationForm()
		args = {'form':form}
		args.update(csrf(request))
		args['form'] = MyRegistrationForm()
		return render(request,'accounts/register.html',args)

def success(request):
	return render(request,'accounts/success.html')



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request,'accounts/valid.html')
    else:
    	return render(request,'accounts/invalid.html')
@csrf_protect
def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/accounts/login/')
@csrf_protect
def forgot_view(request):
	return render(request,'freelance/forgot-password.html')
@csrf_protect
def reset_view(request):
	form = PasswordResetForm(request.POST or None)
	if form.is_valid():
		return render(request,"accounts/referal.html")
	else:
		return render(request,'freelance/forgot-password.html',{"form":form})
def refer_view(request):
	return render(request, 'accounts/referal.html')