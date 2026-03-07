from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('', views.ProductionListView.as_view(), name='production_list'),
    path('<int:pk>/', views.ProductionDetailView.as_view(), name='production_detail'),
    path('ajouter/', views.ProductionCreateView.as_view(), name='production_create'),
    path('<int:pk>/modifier/', views.ProductionUpdateView.as_view(), name='production_update'),
    path('<int:pk>/supprimer/', views.ProductionDeleteView.as_view(), name='production_delete'),
]
