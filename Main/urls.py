from django.urls import path
from . import views

#insert your views here

urlpatterns = [
    path('', views.main, name="main"),
    path('members/', views.members, name="members"),
    path('members/details/<int:id>', views.details, name="details"),
    path('contact/', views.contact, name="contact"),
    path('search/', views.search_view, name='search_results'),


    # path(login/ login/ [name:='login']),
    # path(login/ logout/ [name='logout']),
    # path(login/ password_change/ [name='password_change']),
    # path(login/ password_change/done/ [name='password_change_done']),
    # path(login/ password_reset/ [name='password_reset']),
    # path(login/ password_reset/done/ [name='password_reset_done']),
    # path(login/ reset/<uidb64>/<token>/ [name='password_reset_confirm']),
    # path(login/ reset/done/ [name='password_reset_complete']),
    # (r'^contact/$', 'mysite.books.views.contact'),
]
