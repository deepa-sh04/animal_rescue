from django.shortcuts import render

def home(request):
    return render(request, 'animal_rescue/base.html')