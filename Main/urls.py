from django.urls import path
from . import views

#insert your views here

urlpatterns = [
    path('', views.main, name="main"),
    path('members/', views.members, name="members"),
    path('members/details/<int:id>', views.details, name="details"),
    path('contact/', views.contact, name="contact"),
    # (r'^contact/$', 'mysite.books.views.contact'),
]
