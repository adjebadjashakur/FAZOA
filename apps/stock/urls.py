from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.StockListView.as_view(), name='stock_list'),
    path('<int:pk>/', views.StockDetailView.as_view(), name='stock_detail'),
    path('ajouter/', views.StockCreateView.as_view(), name='stock_create'),
    path('<int:pk>/modifier/', views.StockUpdateView.as_view(), name='stock_update'),
    path('<int:pk>/supprimer/', views.StockDeleteView.as_view(), name='stock_delete'),
    
    # Stock Movement URLs (Block 4)
    path('mouvements/', views.StockMovementListView.as_view(), name='movement_list'),
    path('mouvements/<int:pk>/', views.StockMovementDetailView.as_view(), name='movement_detail'),
    path('<int:pk>/historique/', views.StockMovementHistoryView.as_view(), name='movement_history'),
    path('mouvements/export/', views.StockMovementExportView.as_view(), name='movement_export'),
]
