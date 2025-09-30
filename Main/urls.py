from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('purchaseupdate/', views.purchase, name="purchase"),
    path('partner-with-us/', views.register_partner, name='partner'),
    path('stores-list/', views.stores_list, name="stores"),
    path('prices/', views.prices_combined, name="prices"),
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt",
        content_type="text/plain"
    )),
    path("sitemap.xml", TemplateView.as_view(
        template_name="sitemap.xml",
        content_type="application/xml"
    ), name="sitemap"),
    path('privacy-policy/', views.privacy_policy, name="privacy"),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('csv_download/', views.csv_download, name='csv'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chat/send/', views.chatbot, name='chatbot'),
    path('prices/states/<path:state>/', views.states_listing, name='states_listing'),
    path('members/details/<int:id>/', views.details, name="details"),
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"),
    path('search/', views.search_view, name='search_results'),
]
