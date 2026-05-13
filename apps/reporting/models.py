from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


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
        verbose_name=_('Type de rapport'),
        db_index=True
    )
    
    description = models.TextField(blank=True, verbose_name=_('Description'))
    start_date = models.DateField(verbose_name=_('Date de début'))
    end_date = models.DateField(verbose_name=_('Date de fin'))
    
    data = models.JSONField(null=True, blank=True, verbose_name=_('Données'))
    generated_by = models.CharField(max_length=255, blank=True, verbose_name=_('Généré par'))
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Généré le'), db_index=True)
    
    class Meta:
        verbose_name = _('Rapport')
        verbose_name_plural = _('Rapports')
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['report_type', '-generated_at']),
        ]

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.name}"


class ReportLine(models.Model):
    """Structured report metrics (replaces generic JSONField)."""
    
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name=_('Rapport')
    )
    
    metric_name = models.CharField(
        max_length=255,
        verbose_name=_('Nom de la métrique'),
        db_index=True
    )
    metric_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('Valeur'),
        default=Decimal('0.00')
    )
    unit = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Unité'),
        help_text=_('ex: CFA, %, units')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Créé le'),
        db_index=True
    )

    class Meta:
        verbose_name = _('Ligne de rapport')
        verbose_name_plural = _('Lignes de rapport')
        ordering = ['-created_at']
        unique_together = [['report', 'metric_name']]
        indexes = [
            models.Index(fields=['report', '-created_at']),
        ]

    def __str__(self):
        return f"{self.metric_name}: {self.metric_value} {self.unit}"
