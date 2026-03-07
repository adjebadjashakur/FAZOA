from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.commandes.models import Commande


class Production(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        ACTIVE = 'ACTIVE', _('En cours')
        PAUSED = 'PAUSED', _('Mise en pause')
        COMPLETED = 'COMPLETED', _('Terminée')
        CANCELLED = 'CANCELLED', _('Annulée')

    commande = models.OneToOneField(Commande, on_delete=models.CASCADE, related_name='production', verbose_name=_('Commande'))
    start_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Date de début'))
    end_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Date de fin'))
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('Statut')
    )
    
    produced_quantity = models.PositiveIntegerField(default=0, verbose_name=_('Quantité produite'))
    defective_quantity = models.PositiveIntegerField(default=0, verbose_name=_('Quantité défectueuse'))
    quality_notes = models.TextField(blank=True, verbose_name=_('Notes de qualité'))
    
    assigned_team = models.CharField(max_length=255, blank=True, verbose_name=_('Équipe assignée'))
    line_number = models.CharField(max_length=50, blank=True, verbose_name=_('Numéro de ligne'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Créé le'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Mis à jour le'))

    class Meta:
        verbose_name = _('Production')
        verbose_name_plural = _('Productions')
        ordering = ['-created_at']

    def __str__(self):
        return f"Production - {self.commande.order_number}"
