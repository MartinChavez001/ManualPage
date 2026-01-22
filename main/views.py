from django.shortcuts import render
from .models import Manual

def index(request):
    manuals = Manual.objects.all()
    return render(request, 'main/index.html', {'manuals' : manuals})