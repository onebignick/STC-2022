import welcome.functions as users
from hashlib import sha512

# Django imports here
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

# Create your views here.
def login(request):
    template = "login.html"
    context = {
        "title": "Login page",
    }

    if request.method == "GET":
        return render(request, template, context)

    elif request.method == "POST":

        # Get variables in the form
        username = request.POST.get("exampleInputUsername1")
        password = hashinfo(request.POST.get("exampleInputPassword1"), username)

        session_address = users.login(username, password)
        print(session_address)
        # if username does not exist
        if session_address == "0x0000000000000000000000000000000000000000":
            print("Error! Username or password incorrect")
            context["incorrectDetails"] = True
            return render(request, template, context)

        return redirect("dashboard", username=username, session=session_address)


def signup(request):
    template = "signup.html"
    context = {
        "title": "Sign up page",
    }
    if request.method == "GET":
        return render(request, template, context)

    elif request.method == "POST":
        # Get variables in the form
        username = request.POST.get("signUpUsername1")
        password = hashinfo(request.POST.get("signUpPassword1"), username)
        password_confirm = hashinfo(request.POST.get("signUpPassword2"), username)

        # If passwords don't match
        if password != password_confirm:
            context["noPasswordMatch"] = True
            return render(request, template, context)

        # If username doesn't exist create new user
        try:
            # Hash information and add to blockchain
            users.createNewUser(username, password)
        # Username is taken
        except:
            context["usernameExists"] = True
            return render(request, template, context)

        return redirect(login)


def dashboard(request, username, session):
    if session == "0x0000000000000000000000000000000000000000":
        return redirect(login)

    template = "dashboard.html"
    context = {
        "title": "Dashboard",
        "session": session,
    }
    return render(request, template, context)


def accounts(request):
    template = "accounts.html"
    context = {
        "title": "Accounts",
    }
    return render(request, template, context)


def sessions(request):
    template = "sessions.html"
    context = {
        "title": "sessions",
    }
    return render(request, template, context)


def hashinfo(*args, **kwargs):
    hash = sha512()
    for arg in args:
        hash.update(arg.encode())
    for key, value in kwargs.items():
        hash.update(value.encode())
    return hash.hexdigest()
