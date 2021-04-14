from django.urls import path
from . import views

urlpatterns = [
    #latest update result
    path('equity/bse/', views.EquitiesView.as_view()),
    path('equity/bse/search',views.EquitiesView.as_view()),
    #date specified result
    path('equity/bse/date/<slug:date>/', views.EquitiesView.as_view()),
    path('equity/bse/date/<slug:date>/search', views.EquitiesView.as_view()),
]