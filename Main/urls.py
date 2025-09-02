from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('purchaseupdate/', views.purchase, name="purchase"),
    path('prices/', views.prices_combined, name="prices"),
    path('prices/states/<str:state>/', views.states_listing, name='states_listing'),
    path('food-count/', views.food_count, name='food_count'),
    path('members/details/<int:id>/', views.details, name="details"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('search/', views.search_view, name='search_results'),
]
