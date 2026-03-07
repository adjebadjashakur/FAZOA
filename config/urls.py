from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.users.views import custom_403, custom_404

handler403 = custom_403
handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls', namespace='users')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('clients/', include('apps.clients.urls', namespace='clients')),
    path('commandes/', include('apps.commandes.urls', namespace='commandes')),
    path('stock/', include('apps.stock.urls', namespace='stock')),
    path('production/', include('apps.production.urls', namespace='production')),
    path('ressources/', include('apps.ressources.urls', namespace='ressources')),
    path('reporting/', include('apps.reporting.urls', namespace='reporting')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
