from django.urls import path
from django.conf.urls import url
from . import views
from .views import ChickRestaurant, ProductView


urlpatterns = [
    url('viewrestaurants/', ProductView.as_view(), name='food'),
    path('chevchicken/', views.render_chicken),
    path('booked/', views.render_booking),
    path('sms/', views.sms),
    path('', views.index),
    path('ChevChickenRest/', views.ChickRestaurant)
]
