from django.urls import path
from . import views

app_name = 'ressources'

urlpatterns = [
    path('', views.RessourceListView.as_view(), name='ressource_list'),
    path('<int:pk>/', views.RessourceDetailView.as_view(), name='ressource_detail'),
    path('ajouter/', views.RessourceCreateView.as_view(), name='ressource_create'),
    path('<int:pk>/modifier/', views.RessourceUpdateView.as_view(), name='ressource_update'),
    path('<int:pk>/supprimer/', views.RessourceDeleteView.as_view(), name='ressource_delete'),
]
