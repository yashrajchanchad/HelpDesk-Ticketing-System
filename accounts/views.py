from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate


def login(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('helpdeskapp:index')
        
        return redirect(request.path)

    return render(request, "accounts/login.html")

# def tryu(request):
#     if request.method == "POST":
#         pass
#     return render(request, 'base.html')