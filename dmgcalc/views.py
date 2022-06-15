from django.shortcuts import render
from .models import Champion

# Create your views here.

def dmgcalc(request):
    all_items = Champion.objects.all()
    return render(request, 'index.html', {'all_items': all_items })
