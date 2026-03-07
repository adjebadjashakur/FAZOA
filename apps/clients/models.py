from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Actif')
        INACTIVE = 'INACTIVE', _('Inactif')
        SUSPENDED = 'SUSPENDED', _('Suspendu')

    name = models.CharField(max_length=255, verbose_name=_('Nom du client'))
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    phone = models.CharField(max_length=20, verbose_name=_('Téléphone'))
    address = models.TextField(verbose_name=_('Adresse'))
    city = models.CharField(max_length=100, verbose_name=_('Ville'))
    postal_code = models.CharField(max_length=10, verbose_name=_('Code postal'))
    country = models.CharField(max_length=100, default='Togo', verbose_name=_('Pays'))
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name=_('Statut')
    )
    
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date d\'inscription'))
    last_updated = models.DateTimeField(auto_now=True, verbose_name=_('Dernière mise à jour'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = ['-registration_date']

    def __str__(self):
        return self.name
