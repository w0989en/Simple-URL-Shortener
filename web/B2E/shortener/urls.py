from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create', views.create),
    path('create/success', views.create_success),
    path('<str:short_url>', views.short_url_redirect),
]
