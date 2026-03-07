from django.urls import path
from . import views

app_name = 'reporting'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report_list'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('ajouter/', views.ReportCreateView.as_view(), name='report_create'),
    path('<int:pk>/modifier/', views.ReportUpdateView.as_view(), name='report_update'),
    path('<int:pk>/supprimer/', views.ReportDeleteView.as_view(), name='report_delete'),
]
