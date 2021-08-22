
from django.urls import path

from food import views, views1

urlpatterns = [
    path('',views.index,name='index'),
    path('UpdateDashboard',views.UpdateDashboard,name="UpdateDashboard"),
    path('statewise/<state>',views1.statewise,name='statewise'),
    path('VegNonveg',views1.VegNonveg,name='VegNonveg')
]
