from django.urls import path
from . import views

urlpatterns = [
    #latest update result
    path('equity/', views.EquitiesView.as_view()),
    path('equity/search/',views.EquitiesView.as_view()),
    #date specified result
    path('equity/date/<slug:date>/', views.EquitiesView.as_view()),
    path('equity/date/<slug:date>/search/', views.EquitiesView.as_view()),
]