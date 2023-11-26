from django.urls import path, include
from . import views

urlpatterns = [
    path('osoby/', views.osoba_list),
    path('osoby/<int:pk>/', views.osoba_detail),
    path('osoby/update/<int:pk>/', views.osoba_update),
    path('osoby/delete/<int:pk>', views.osoba_delete),
    path('stanowiska/', views.stanowisko_list),
    path('stanowiska/<int:pk>/', views.stanowisko_detail),
    path('stanowiska/<int:pk>/members/', views.stanowisko_members),
]
