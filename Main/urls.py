from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

#insert your views here

urlpatterns = [
    path('', views.main, name="main"),
    path('purchaseupdate/', views.purchase, name="purchase"),
    path('prices/', views.prices, name="prices"),
    path('food-count/', views.food_count, name='food_count'),
    #path('members/', views.members, name="members"),
    path('members/details/<int:id>', views.details, name="details"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('search/', views.search_view, name='search_results'),
    path('accounts/', include('django.contrib.auth.urls')), # This includes login, logout, password reset, etc.
    path('accounts/login/', views.login, name='login'), # Custom view for the login path


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
