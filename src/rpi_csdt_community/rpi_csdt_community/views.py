from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    return render_to_response('home.html', {"form": AuthenticationForm()}, context_instance=RequestContext(request))
