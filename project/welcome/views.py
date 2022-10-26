import welcome.deploy as deploy

# Django imports here
from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def home(request):
    template = "index.html"
    return render(request, template)


def login(request):
    template = "welcome/login.html"
    return render(request, template)


def signup(request):
    template = "welcome/signup.html"
    context = {
        "title": "Sign up page",
    }
    if request.method == "GET":
        return render(request, template, context)

    elif request.method == "POST":
        # Get variables in the form
        username = request.POST.get("signUpUsername1")
        # request.session["username"] = username

        password = request.POST.get("signUpPassword1")
        # request.session["password"] = password

        password_confirm = request.POST.get("signUpPassword2")
        # request.session["password_confirm"] = password_confirm

        # If passwords don't match
        if password != password_confirm:
            context["noPasswordMatch"] = True
            return render(request, template, context)

        # If username doesn't exist create new user
        if deploy.findPassword(username) == "0":
            deploy.createNewUser(username, password)

        # Else username is already taken
        else:
            context["usernameExists"] = True
        return render(request, template, context)
