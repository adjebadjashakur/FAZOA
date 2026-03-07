from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.ClientListView.as_view(), name='client_list'),
    path('<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('ajouter/', views.ClientCreateView.as_view(), name='client_create'),
    path('<int:pk>/modifier/', views.ClientUpdateView.as_view(), name='client_update'),
    path('<int:pk>/supprimer/', views.ClientDeleteView.as_view(), name='client_delete'),
]
