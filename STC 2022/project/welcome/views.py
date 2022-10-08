from django.shortcuts import render

# Create your views here.
def home(request):
    template = "index.html"
    return render(request, template)
