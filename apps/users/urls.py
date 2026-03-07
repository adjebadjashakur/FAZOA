from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('utilisateurs/', views.UserListView.as_view(), name='user_list'),
    path('utilisateurs/ajouter/', views.UserCreateView.as_view(), name='user_create'),
    path('utilisateurs/<int:pk>/modifier/', views.UserUpdateView.as_view(), name='user_update'),
    path('utilisateurs/<int:pk>/supprimer/', views.UserDeleteView.as_view(), name='user_delete'),
]
