from django.shortcuts import render, redirect
from .models import Graphs,Data
def statewise(request,state):
    items=Data.objects.filter(State=state)
    context={
        'items':items,
        'state':state
    }
    return render(request,'statewise.html',context)

def VegNonveg(request):
    veg=Data.objects.filter(Diet="vegetarian")
    nonveg=Data.objects.filter(Diet='non vegetarian')
    context={
        'vegs': veg,
        'nonveg':nonveg
    }
    return render(request,'VegNonveg.html',context)