import welcome.functions as users
from hashlib import sha512

# Django imports here
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

# Initialise the cookie jar
cj = {}  # primitive cookie jar

# Create your views here.
def login(request):
    template = "login.html"
    context = {
        "title": "Login page",
    }

    if request.method == "GET":
        response = render(request, template, context)
        return response

    elif request.method == "POST":

        # Get variables in the form
        username = request.POST.get("exampleInputUsername1")
        password = hashinfo(request.POST.get("exampleInputPassword1"), username)

        session_address = users.login(username, password)
        # if username does not exist
        if session_address == "0x0000000000000000000000000000000000000000":
            print("Error! Username or password incorrect")
            context["incorrectDetails"] = True
            response = render(request, template, context)
            return response

        response = redirect(dashboard)
        cj["session"] = session_address

        # session cookie for user, password is hashed
        response.set_cookie("session", session_address)
        # add logic to change auth level, 1 = normal user, 2 = admin
        response.set_cookie("authlevel", "1")
        return response


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
        password = request.POST.get("signUpPassword1")
        password_confirm = request.POST.get("signUpPassword2")

        # If passwords don't match
        if password != password_confirm:
            context["noPasswordMatch"] = True
            return render(request, template, context)

        password = hashinfo(password, username)

        # If username doesn't exist create new user
        try:
            # Hash information and add to blockchain
            users.createNewUser(username, password)
        # Username is taken
        except:
            context["usernameExists"] = True
            return render(request, template, context)

        return redirect(login)


def dashboard(request):
    current_session = request.COOKIES.get("session")
    if current_session == "0x0000000000000000000000000000000000000000":
        return redirect(login)

    template = "dashboard.html"
    context = {
        "title": "Dashboard",
        "username": users.getUsername(current_session),
        "session": current_session,
    }
    return render(request, template, context)


def accounts(request):
    template = "accounts.html"
    all_accounts = users.getAllUsers()
    context = {
        "title": "Accounts",
        "all_accounts": all_accounts,
    }
    return render(request, template, context)


def sessions(request):
    template = "sessions.html"
    context = {
        "title": "sessions",
    }
    return render(request, template, context)


def logout(request):
    session = request.COOKIES.get("session")
    print(users.logout(users.getUsername(session), session))
    return redirect(login)


# Test page for cookies, you can only view this page if you have a valid session cookie
def secure(request):
    context = {
        "title": "Secure",
        "auth": 0,
    }
    template = "secure.html"
    if "session" not in cj:
        return render(request, template, context)
    else:
        if request.COOKIES.get("session") not in cj["session"]:
            return render(request, template, context)
    # testing admin cookie
    if request.COOKIES.get("authlevel") == "2":
        context["auth"] = 2
    else:
        context["auth"] = 1
    return render(request, template, context)


def hashinfo(*args, **kwargs):
    hash = sha512()
    for arg in args:
        hash.update(arg.encode())
    for key, value in kwargs.items():
        hash.update(value.encode())
    return hash.hexdigest()
