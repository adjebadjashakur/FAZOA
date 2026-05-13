from django.contrib import admin
from .models import KPISnapshot, KPIDashboardConfig


@admin.register(KPISnapshot)
class KPISnapshotAdmin(admin.ModelAdmin):
    list_display = ['metric_type', 'metric_value', 'unit', 'captured_at']
    list_filter = ['metric_type', 'captured_at']
    search_fields = ['metric_type']
    ordering = ['-captured_at']
    readonly_fields = ['captured_at']

    fieldsets = [
        ('Métrique', {
            'fields': ['metric_type', 'metric_value', 'unit']
        }),
        ('Métadonnées', {
            'fields': ['metadata']
        }),
        ('Audit', {
            'fields': ['captured_at']
        }),
    ]


@admin.register(KPIDashboardConfig)
class KPIDashboardConfigAdmin(admin.ModelAdmin):
    list_display = ['user_role', 'default_chart_type', 'refresh_interval_minutes']
    fieldsets = [
        ('Configuration', {
            'fields': ['user_role', 'default_chart_type', 'refresh_interval_minutes']
        }),
        ('Visibilité des métriques', {
            'fields': ['show_revenue', 'show_orders', 'show_production', 'show_stock', 'show_resources']
        }),
    ]
