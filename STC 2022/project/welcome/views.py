from django.shortcuts import render

# Create your views here.
def home(request):
    template = "index.html"
    return render(request, template)


def login(request):
    template = "welcome/login.html"
    return render(request, template)
