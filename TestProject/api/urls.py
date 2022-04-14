from django.urls import path

from . import views

urlpatterns = [
    path("message/", views.AddMessage.as_view()),
    path("message_confirmation/", views.CheckMessage.as_view()),
    path("jwt/", views.GetJwtToken.as_view()),
]