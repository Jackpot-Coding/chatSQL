from django.shortcuts import redirect,render
from .promptGenerator import *

def main(request):
    return render(request,"index.html")

def responseITA(request):
    if request.method!="POST":
        return redirect("/")
    natural=request.POST["natural"]
    context = {
        'promptresponse': generatePromptITA(natural),
    }
    return render(request,"response.html",context)

def responseENG(request):
    if request.method!="POST":
        return redirect("/")
    natural=request.POST["natural"]
    context = {
        'promptresponse': generatePromptENG(natural),
    }
    return render(request,"response.html",context)