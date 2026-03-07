from django.contrib import admin
from .models import Ressource


@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'resource_type', 'status', 'location', 'capacity', 'cost', 'maintenance_date']
    list_filter = ['resource_type', 'status']
    search_fields = ['name', 'location']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Informations générales', {
            'fields': ['name', 'description', 'resource_type', 'status']
        }),
        ('Détails', {
            'fields': ['location', 'capacity', 'cost']
        }),
        ('Dates', {
            'fields': ['acquisition_date', 'maintenance_date', 'created_at', 'updated_at']
        }),
        ('Notes', {
            'fields': ['notes']
        }),
    ]
    