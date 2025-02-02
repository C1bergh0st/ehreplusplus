from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from counter.models import UserValues

from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.save()
            profile = UserValues.objects.create(user=user)
            profile.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
