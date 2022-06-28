from django.urls import path
from . import views

urlpatterns = [
    path('', views.dmgcalc_function, name='dmgcalc'),
]
