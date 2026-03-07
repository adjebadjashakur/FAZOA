from django.contrib import admin
from .models import Production


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = [
        'commande', 'status', 'produced_quantity', 'defective_quantity',
        'assigned_team', 'line_number', 'start_date', 'end_date'
    ]
    list_filter = ['status', 'assigned_team']
    search_fields = ['commande__order_number', 'assigned_team', 'line_number']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Commande liée', {
            'fields': ['commande', 'status']
        }),
        ('Équipe & Ligne', {
            'fields': ['assigned_team', 'line_number']
        }),
        ('Quantités', {
            'fields': ['produced_quantity', 'defective_quantity']
        }),
        ('Dates', {
            'fields': ['start_date', 'end_date', 'created_at', 'updated_at']
        }),
        ('Notes', {
            'fields': ['quality_notes', 'notes']
        }),
    ]