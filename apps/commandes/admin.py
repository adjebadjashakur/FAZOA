# apps/commandes/admin.py
from django.contrib import admin
from .models import Commande


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'client', 'quantity', 
        'unit_price', 'total_price', 'status', 'order_date', 'expected_delivery'
    ]
    
    list_filter = ['status', 'order_date', 'expected_delivery']
    
    search_fields = ['order_number', 'client__name', 'description']
    
    ordering = ['-order_date']
    
    readonly_fields = ['order_date']
    
    # Permet de modifier le statut directement depuis la liste
    list_editable = ['status']
    
    fieldsets = [
        ('Informations de la commande', {
            'fields': ['client', 'order_number', 'description', 'status']
        }),
        ('Détails financiers', {
            'fields': ['quantity', 'unit_price', 'total_price']
        }),
        ('Dates', {
            'fields': ['order_date', 'expected_delivery', 'actual_delivery']
        }),
        ('Autres', {
            'fields': ['notes']
        }),
    ]
    
    # Calcul automatique du total depuis la liste
    def save_model(self, request, obj, form, change):
        obj.total_price = obj.quantity * obj.unit_price
        super().save_model(request, obj, form, change)