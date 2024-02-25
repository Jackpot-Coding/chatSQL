from django.template import loader
from django.http import HttpResponse
from .models import *

def main(request):    
    template=loader.get_template("index.html")
    context = {
        'username': getUsername(),
    }
    return HttpResponse(template.render(context,request))

def responseITA(request):
    template=loader.get_template("response.html")
    if request.method=="POST":
        natural=request.POST["natural"]
    context = {
        'username': getUsername(),
        'promptresponse': generatePromptITA(natural),
    }
    return HttpResponse(template.render(context,request))

def responseENG(request):
    template=loader.get_template("response.html")
    if request.method=="POST":
        natural=request.POST["natural"]
    context = {
        'username': getUsername(),
        'promptresponse': generatePromptENG(natural),
    }
    return HttpResponse(template.render(context,request))