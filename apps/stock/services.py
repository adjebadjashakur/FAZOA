"""
Stock management services for atomic operations and history tracking.
"""
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from .models import Stock, StockMovement


@transaction.atomic
def mouvementer_stock(
    stock,
    quantity,
    movement_type,
    reason='',
    reference_type='',
    reference_id=None,
    created_by=None
):
    """
    Atomic stock movement with history tracking.
    
    Args:
        stock: Stock instance to move
        quantity: Integer (can be negative for outflows)
        movement_type: One of ENTREE, SORTIE, AJUSTEMENT, INVENTAIRE
        reason: Optional reason for the movement
        reference_type: Optional type (COMMANDE, PRODUCTION, etc.)
        reference_id: Optional ID of the reference object
        created_by: User instance who made the movement
    
    Returns:
        StockMovement instance created
        
    Raises:
        ValueError: If quantity would result in negative stock (except INVENTAIRE)
    """
    quantity_before = stock.quantity
    quantity_after = quantity_before + quantity
    
    # Validate stock doesn't go negative (unless it's an inventory adjustment)
    if movement_type != 'INVENTAIRE' and quantity_after < 0:
        raise ValueError(
            f'Mouvement invalide: {quantity_before} {quantity:+d} = {quantity_after} (négatif)'
        )
    
    # Update stock quantity
    stock.quantity = quantity_after
    stock.save(update_fields=['quantity', 'updated_at'])
    
    # Create movement record
    movement = StockMovement.objects.create(
        stock=stock,
        movement_type=movement_type,
        quantity_before=quantity_before,
        quantity_after=quantity_after,
        quantity_changed=quantity,
        reason=reason,
        reference_type=reference_type,
        reference_id=reference_id,
        created_by=created_by,
    )
    
    return movement
