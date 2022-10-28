import welcome.functions as users
from hashlib import sha512

# Django imports here
from django.shortcuts import render, redirect, HttpResponse

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
        # request.session["username"] = username

        password = request.POST.get("exampleInputPassword1")
        # request.session["password"] = password

        # if username does not exist
        print(users.findPassword(username))
        if users.findPassword(username) == None:
            print("User does not exist")
            context["usernameExists"] = True
            return render(request, template, context)

        # if password does not match user
        elif users.findPassword(username) != hashinfo(password, username):
            print("Incorrect Password")
            context["correctPassword"] = True
            return render(request, template, context)

        return render(request, template, context)


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
       

def dashboard(request):
    template = "welcome/dashboard.html"
    context = {
        "title": "Dashboard",
    }
    return render(request, template, context)


def hashinfo(*args):
    hash = sha512()
    for arg in args:
        hash.update(arg.encode())
    return hash.hexdigest()
