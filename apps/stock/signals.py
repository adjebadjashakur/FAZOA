"""
Stock signals for automatic tracking.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.commandes.models import Commande
from .models import Stock, StockMovement
from .services import mouvementer_stock


@receiver(post_save, sender=Commande)
def create_stock_movement_on_confirmation(sender, instance, created, update_fields, **kwargs):
    """
    Auto-create stock movements when commande status changes to CONFIRMED.
    This tracks outflows from inventory when orders are confirmed.
    
    Note: Full integration with production and fulfillment flows would
    require additional logic in production and shipment signals.
    """
    # Only process updates (not creates) and only if status changed
    if created or not update_fields or 'status' not in update_fields:
        return
    
    # If status changed to CONFIRMED, would create stock movements here
    # For now, this is a placeholder for the full integration
    # The actual stock movements should be created when:
    # - Commande.status → CONFIRMED: Create SORTIE movements for allocated items
    # - Production.status → COMPLETED: Create ENTREE movements for finished goods
    pass
