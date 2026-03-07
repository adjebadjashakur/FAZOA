from django.urls import path
from . import views

app_name = 'commandes'

urlpatterns = [
    path('', views.CommandeListView.as_view(), name='commande_list'),
    path('<int:pk>/', views.CommandeDetailView.as_view(), name='commande_detail'),
    path('ajouter/', views.CommandeCreateView.as_view(), name='commande_create'),
    path('<int:pk>/modifier/', views.CommandeUpdateView.as_view(), name='commande_update'),
    path('<int:pk>/supprimer/', views.CommandeDeleteView.as_view(), name='commande_delete'),
]
