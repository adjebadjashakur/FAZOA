from django.db import models
from django.utils.translation import gettext_lazy as _


class Ressource(models.Model):
    class Type(models.TextChoices):
        EQUIPMENT = 'EQUIPMENT', _('Équipement')
        PERSONNEL = 'PERSONNEL', _('Personnel')
        FACILITY = 'FACILITY', _('Installation')
        SOFTWARE = 'SOFTWARE', _('Logiciel')

    name = models.CharField(max_length=255, verbose_name=_('Nom de la ressource'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    
    resource_type = models.CharField(
        max_length=20,
        choices=Type.choices,
        verbose_name=_('Type de ressource')
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('AVAILABLE', _('Disponible')),
            ('IN_USE', _('En utilisation')),
            ('MAINTENANCE', _('Maintenance')),
            ('UNAVAILABLE', _('Indisponible')),
        ],
        default='AVAILABLE',
        verbose_name=_('Statut')
    )
    
    location = models.CharField(max_length=255, blank=True, verbose_name=_('Localisation'))
    capacity = models.CharField(max_length=255, blank=True, verbose_name=_('Capacité'))
    
    acquisition_date = models.DateField(null=True, blank=True, verbose_name=_('Date d\'acquisition'))
    maintenance_date = models.DateField(null=True, blank=True, verbose_name=_('Dernier entretien'))
    
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Coût'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Créé le'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Mis à jour le'))

    class Meta:
        verbose_name = _('Ressource')
        verbose_name_plural = _('Ressources')
        ordering = ['name']

    def __str__(self):
        return self.name
