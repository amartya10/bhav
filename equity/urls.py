from django.urls import path
from . import views

urlpatterns = [
    path('equity/bse/', views.EquitiesView.as_view()),
]