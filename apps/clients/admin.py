
from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'city', 'country', 'status', 'registration_date']
    
    list_filter = ['status', 'country', 'city']
    
    search_fields = ['name', 'email', 'phone', 'city']
    
    ordering = ['-registration_date']
    
    readonly_fields = ['registration_date', 'last_updated']
    
    fieldsets = [
        ('Informations générales', {
            'fields': ['name', 'email', 'phone', 'status']
        }),
        ('Adresse', {
            'fields': ['address', 'city', 'postal_code', 'country']
        }),
        ('Autres', {
            'fields': ['notes', 'registration_date', 'last_updated']
        }),
    ]