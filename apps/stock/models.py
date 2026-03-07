from django.db import models
from django.utils.translation import gettext_lazy as _


class Stock(models.Model):
    class Category(models.TextChoices):
        RAW_MATERIALS = 'RAW_MATERIALS', _('Matières premières')
        FINISHED_GOODS = 'FINISHED_GOODS', _('Produits finis')
        SPARE_PARTS = 'SPARE_PARTS', _('Pièces détachées')

    sku = models.CharField(max_length=50, unique=True, verbose_name=_('SKU'))
    name = models.CharField(max_length=255, verbose_name=_('Nom du produit'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.RAW_MATERIALS,
        verbose_name=_('Catégorie')
    )
    
    quantity = models.PositiveIntegerField(verbose_name=_('Quantité'))
    minimum_quantity = models.PositiveIntegerField(default=10, verbose_name=_('Quantité minimale'))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Prix unitaire'))
    
    last_restock = models.DateField(null=True, blank=True, verbose_name=_('Dernier réapprovisionnement'))
    supplier = models.CharField(max_length=255, blank=True, verbose_name=_('Fournisseur'))
    location = models.CharField(max_length=100, blank=True, verbose_name=_('Localisation'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Créé le'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Mis à jour le'))

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def needs_restock(self):
        return self.quantity <= self.minimum_quantity
