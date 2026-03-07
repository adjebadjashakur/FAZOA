from django.contrib import admin
from .models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'quantity', 'minimum_quantity', 'unit_price', 'supplier', 'needs_restock']
    list_filter = ['category', 'supplier']
    search_fields = ['name', 'sku', 'supplier']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Informations produit', {
            'fields': ['name', 'sku', 'description', 'category']
        }),
        ('Stock & Prix', {
            'fields': ['quantity', 'minimum_quantity', 'unit_price']
        }),
        ('Fournisseur & Localisation', {
            'fields': ['supplier', 'location', 'last_restock']
        }),
        ('Autres', {
            'fields': ['notes', 'created_at', 'updated_at']
        }),
    ]

    # Alerte visuelle si stock bas
    def needs_restock(self, obj):
        if obj.needs_restock:
            return '⚠️ Réapprovisionner'
        return '✅ OK'
    needs_restock.short_description = 'État du stock'