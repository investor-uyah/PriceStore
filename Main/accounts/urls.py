from django.urls import path
from django.contrib.auth.views import LogoutView # Import built-in views
from .. import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout')

]
