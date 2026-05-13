from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Stock(models.Model):
    class Category(models.TextChoices):
        RAW_MATERIALS = 'RAW_MATERIALS', _('Matières premières')
        FINISHED_GOODS = 'FINISHED_GOODS', _('Produits finis')
        SPARE_PARTS = 'SPARE_PARTS', _('Pièces détachées')

    sku = models.CharField(max_length=50, unique=True, verbose_name=_('SKU'), db_index=True)
    name = models.CharField(max_length=255, verbose_name=_('Nom du produit'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.RAW_MATERIALS,
        verbose_name=_('Catégorie'),
        db_index=True
    )
    
    quantity = models.PositiveIntegerField(verbose_name=_('Quantité'))
    minimum_quantity = models.PositiveIntegerField(default=10, verbose_name=_('Quantité minimale'))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Prix unitaire'))
    
    last_restock = models.DateField(null=True, blank=True, verbose_name=_('Dernier réapprovisionnement'))
    supplier = models.CharField(max_length=255, blank=True, verbose_name=_('Fournisseur'))
    location = models.CharField(max_length=100, blank=True, verbose_name=_('Localisation'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Créé le'), db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Mis à jour le'))

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')
        ordering = ['name']
        indexes = [
            models.Index(fields=['category', 'quantity']),
            models.Index(fields=['quantity']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def needs_restock(self):
        return self.quantity <= self.minimum_quantity


class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        ENTREE = 'ENTREE', _('Entrée')
        SORTIE = 'SORTIE', _('Sortie')
        AJUSTEMENT = 'AJUSTEMENT', _('Ajustement')
        INVENTAIRE = 'INVENTAIRE', _('Inventaire')

    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name='movements',
        verbose_name=_('Stock')
    )
    movement_type = models.CharField(
        max_length=20,
        choices=MovementType.choices,
        verbose_name=_('Type de mouvement'),
        db_index=True
    )
    
    quantity_before = models.PositiveIntegerField(verbose_name=_('Quantité avant'))
    quantity_after = models.PositiveIntegerField(verbose_name=_('Quantité après'))
    quantity_changed = models.IntegerField(verbose_name=_('Quantité modifiée'))
    
    reason = models.TextField(blank=True, verbose_name=_('Raison'))
    reference_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Type de référence'),
        help_text=_('ex: COMMANDE, PRODUCTION')
    )
    reference_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('ID de référence')
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements',
        verbose_name=_('Créé par')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Créé le'),
        db_index=True
    )

    class Meta:
        verbose_name = _('Mouvement de stock')
        verbose_name_plural = _('Mouvements de stock')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['stock', '-created_at']),
            models.Index(fields=['movement_type', '-created_at']),
        ]

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.stock.sku} ({self.quantity_changed:+d})"
