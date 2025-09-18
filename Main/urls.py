from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('purchaseupdate/', views.purchase, name="purchase"),
    path('partner-with-us/', views.register_partner, name='partner'),
    path('stores-list/', views.stores_list, name="stores"),
    path('prices/', views.prices_combined, name="prices"),
    path('privacy-policy/', views.privacy_policy, name="privacy"),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chat/send/', views.chatbot, name='chatbot'),
    path('prices/states/<str:state>/', views.states_listing, name='states_listing'),
    path('members/details/<int:id>/', views.details, name="details"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('search/', views.search_view, name='search_results'),
]
