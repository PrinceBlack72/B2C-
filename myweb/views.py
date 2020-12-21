from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render_to_response

# Create your views here.
def t(request):
    return HttpResponse("Hello World")

def t2(request):
    return render_to_response("./myweb/test.html")