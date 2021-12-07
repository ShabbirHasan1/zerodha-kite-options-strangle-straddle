from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from requests.sessions import session

# Create your views here.
def login(request):
    request_data = request.GET
    next = request_data.get('next')

    if request.user.is_authenticated:
        return redirect(next or reverse('dashboard'))

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            django_login(request, user)

            if not request.POST.get('remember', None):
                request.session.set_expiry(0)
            
            return redirect(next or reverse('dashboard'))
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, 'login.html')

# @login_required(login_url='login')
def logout(request):
    # x = django_logout(request)
    # print(str(x))
    return redirect(reverse('login'))

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'index.html', context={'user': request.user})