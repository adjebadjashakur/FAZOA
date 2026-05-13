from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.clients.models import Client


class Commande(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        CONFIRMED = 'CONFIRMED', _('Confirmée')
        IN_PRODUCTION = 'IN_PRODUCTION', _('En production')
        READY = 'READY', _('Prête')
        SHIPPED = 'SHIPPED', _('Expédiée')
        DELIVERED = 'DELIVERED', _('Livrée')
        CANCELLED = 'CANCELLED', _('Annulée')

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='commandes', verbose_name=_('Client'))
    order_number = models.CharField(max_length=50, unique=True, verbose_name=_('Numéro de commande'), db_index=True)
    description = models.TextField(verbose_name=_('Description'))
    quantity = models.PositiveIntegerField(verbose_name=_('Quantité'))
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('Statut'),
        db_index=True
    )
    
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Prix unitaire'))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Prix total'))
    
    order_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date de commande'))
    expected_delivery = models.DateField(null=True, blank=True, verbose_name=_('Livraison prévue'))
    actual_delivery = models.DateField(null=True, blank=True, verbose_name=_('Livraison réelle'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta:
        verbose_name = _('Commande')
        verbose_name_plural = _('Commandes')
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['client', 'status']),
            models.Index(fields=['status', '-order_date']),
        ]

    def __str__(self):
        return self.order_number
