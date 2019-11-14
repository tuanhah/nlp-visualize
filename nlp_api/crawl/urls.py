from django.urls import path

from . import views

urlpatterns = [
    path('', views.crawlData, name='crawlData'),
    path('custom', views.customData, name='customData'),
]