from django.db import models
from django.utils.translation import gettext_lazy as _


class Report(models.Model):
    class ReportType(models.TextChoices):
        SALES = 'SALES', _('Ventes')
        PRODUCTION = 'PRODUCTION', _('Production')
        STOCK = 'STOCK', _('Stock')
        FINANCIAL = 'FINANCIAL', _('Financier')
        OPERATIONS = 'OPERATIONS', _('Opérations')

    name = models.CharField(max_length=255, verbose_name=_('Nom du rapport'))
    report_type = models.CharField(
        max_length=20,
        choices=ReportType.choices,
        verbose_name=_('Type de rapport')
    )
    
    description = models.TextField(blank=True, verbose_name=_('Description'))
    start_date = models.DateField(verbose_name=_('Date de début'))
    end_date = models.DateField(verbose_name=_('Date de fin'))
    
    data = models.JSONField(null=True, blank=True, verbose_name=_('Données'))
    generated_by = models.CharField(max_length=255, blank=True, verbose_name=_('Généré par'))
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Généré le'))
    
    class Meta:
        verbose_name = _('Rapport')
        verbose_name_plural = _('Rapports')
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.name}"
