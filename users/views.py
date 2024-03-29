from django.shortcuts import render,redirect
from users.forms import UserOurRegistraion, ProfileImage, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from basket.models import Cart
from django.db.models import Sum

def register(request):
	if request.method == "POST":
		form = UserOurRegistraion(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('email')
			messages.success(request, f'Пользовател {username} был успешно создан!')
			return redirect('user')
	else:
		form = UserOurRegistraion()
	return render(request, 'users/register.html', {'form':form, 'title':'Регистрация пользователя'})


@login_required
def profile(request):
	if request.method == 'POST':

		img_profile = ProfileImage(request.POST, request.FILES, instance=request.user.profile)
		update_user	= UserUpdateForm(request.POST, instance=request.user)

		if update_user.is_valid() and img_profile.is_valid():
			update_user.save()
			img_profile.save()
			messages.success(request, f'Ваш аккаунт был успешно обновлен')
			return redirect('profile')
	else:
		img_profile = ProfileImage(instance=request.user.profile)
		update_user = UserUpdateForm(instance=request.user)

	data = {
		'count': Cart.objects.filter(user=request.user.username).count(),
		'sum': Cart.objects.filter(user=request.user.username).aggregate(Sum('price')),
		'img_profile': img_profile,
		'update_user': update_user
	}
	return render(request, 'users/profile.html', data)

