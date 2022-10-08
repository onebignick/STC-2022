import json
from web3 import Web3

# Django imports here
from django.shortcuts import render, redirect, HttpResponse

'''
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Sepolia account
public_key = ""
private_key = ""

# Connecting to infura
url = ""

# Initiating web3
web3 = Web3(Web3.HTTPProvider(url))

# Contract's address and abi
address = web3.toChecksumAddress("")
abi = json.loads("""[]""")

# Creating a contract instance
contract = web3.eth.contract(address=address, abi=abi)
'''

# Create your views here.
def home(request):
    template = "index.html"
    return render(request, template)


def login(request):
    template = "welcome/login.html"
    return render(request, template)


def signup(request):
    template = "welcome/signup.html"
    return render(request, template)
