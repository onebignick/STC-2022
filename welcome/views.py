import welcome.functions as users
from hashlib import sha512

# Django imports here
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from datetime import datetime
import pytz

# Initialise the cookie jar
cj = {}  # primitive cookie jar

# Create your views here.
def login(request):
    print(request.COOKIES)
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
        response.set_cookie("session", session_address, max_age=30 * 60)
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
    if (
        current_session != "0x0000000000000000000000000000000000000000"
        and users.getLoginDatetime(current_session) != 0
        and users.getLogoutDatetime(current_session) == 0
    ):
        username = users.getUsername(current_session)
        role = users.getUser(username)[2]
        var_clicks = users.getUser(username)[3]
        template = "dashboard.html"
        context = {
            "title": "Dashboard",
            "username": username,
            "session": current_session,
            "role": role,
            "var_clicks": var_clicks,
        }
        if request.method == "POST":
            var_clicks = request.POST["var_clicks"]
            users.updateClick(username, int(var_clicks))
            print(var_clicks)

        return render(request, template, context)
    return redirect(login)


def profile(request):
    current_session = request.COOKIES.get("session")
    if (
        current_session != "0x0000000000000000000000000000000000000000"
        and users.getLoginDatetime(current_session) != 0
        and users.getLogoutDatetime(current_session) == 0
    ):
        username = users.getUsername(current_session)
        role = users.getUser(username)[2]

        template = "profile.html"
        context = {
            "title": "Profile",
            "session": current_session,
            "username": username,
            "role": role,
        }
        if request.method == "POST":
            oldPassword = request.POST.get("oldPassword")
            newPassword = request.POST.get("newPassword")
            newPasswordConfirm = request.POST.get("newPasswordConfirm")

            if newPassword != newPasswordConfirm:
                context["Error"] = True
                return render(request, template, context)

            elif users.findPassword(username) != hashinfo(oldPassword, username):
                context["PasswordError"] = True
                return render(request, template, context)
            users.changePassword(username, hashinfo(oldPassword, username), hashinfo(newPassword, username))
            context["PasswordChanged"] = True
            return render(request, template, context)
        return render(request, template, context)
    return redirect(login)


def accounts(request):
    current_session = request.COOKIES.get("session")
    if (
        current_session != "0x0000000000000000000000000000000000000000"
        and users.getLoginDatetime(current_session) != 0
        and users.getLogoutDatetime(current_session) == 0
    ):

        username = users.getUsername(current_session)
        if users.getUser(username)[2] != "admin":
            return redirect(login)

        if request.method == "GET":
            template = "accounts.html"
            all_accounts = users.getAllUsers()
            context = {
                "title": "Accounts",
                "username": username,
                "session": current_session,
                "all_accounts": all_accounts,
            }
            return render(request, template, context)
        
        elif request.method == "POST" and "promote_button" in request.POST:
            username = request.POST.get("userToEdit")
            try:
                users.getUser(username)
                users.giveRole(username, "admin")
            except:
                print("error")
            return redirect(accounts)

        elif request.method == "POST" and "demote_button" in request.POST:
            username = request.POST.get("userToEdit")
            try:
                users.getUser(username)
                users.giveRole(username, "user")
            except:
                print("error")
            return redirect(accounts)

        elif request.method == "POST" and "delete_button" in request.POST:
            username = request.POST.get("userToEdit")
            try:
                users.getUser(username)
                users.deleteUser(username)
            except:
                print("error")
            return redirect(accounts)

        return redirect(login)


def sessions(request):
    current_session = request.COOKIES.get("session")
    if (
        current_session != "0x0000000000000000000000000000000000000000"
        and users.getLoginDatetime(current_session) != 0
        and users.getLogoutDatetime(current_session) == 0
    ):
        username = users.getUsername(current_session)
        if users.getUser(username)[2] != "admin":
            return redirect(login)

        all_sessions = users.getAllSessions()
        all_sessions_info = []

        for i in range(len(all_sessions)):
            loginDateTime = users.getLoginDatetime(all_sessions[i])
            login_obj = datetime.fromtimestamp(loginDateTime)
            

            logoutDateTime = users.getLogoutDatetime(all_sessions[i])
            logout_obj = "Logged in"
            if (logoutDateTime != 0):
                logout_obj = datetime.fromtimestamp(logoutDateTime)
            
            all_sessions_info.append(
                (
                    all_sessions[i],
                    users.getUsername(all_sessions[i]),
                    login_obj,
                    logout_obj,
                )
            )

        template = "sessions.html"
        context = {
            "title": "sessions",
            "session": current_session,
            "sessions": all_sessions_info,
            "user": username
        }
        return render(request, template, context)
    return redirect(login)


def logout(request):
    session = request.COOKIES.get("session")
    print(users.logout(users.getUsername(session), session))
    response = redirect(login)
    response.delete_cookie("session")  # delete cookie on session exit
    return response


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
        if request.COOKIES.get("session") not in cj.values():
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
