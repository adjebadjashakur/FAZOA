from django.contrib import admin
from .models import Stock, StockMovement


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


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['stock', 'movement_type', 'quantity_changed', 'created_by', 'created_at']
    list_filter = ['movement_type', 'created_at']
    search_fields = ['stock__sku', 'stock__name', 'reason']
    ordering = ['-created_at']
    readonly_fields = ['quantity_before', 'quantity_after', 'created_at']

    fieldsets = [
        ('Stock', {
            'fields': ['stock']
        }),
        ('Mouvement', {
            'fields': ['movement_type', 'quantity_before', 'quantity_after', 'quantity_changed', 'reason']
        }),
        ('Référence', {
            'fields': ['reference_type', 'reference_id']
        }),
        ('Audit', {
            'fields': ['created_by', 'created_at']
        }),
    ]
