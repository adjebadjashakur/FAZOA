from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class KPISnapshot(models.Model):
    """
    Store calculated KPI values with timestamp for trend analysis.
    Enables historical tracking of metrics without recalculating.
    """
    
    class MetricType(models.TextChoices):
        REVENUE = 'REVENUE', _('Revenu total')
        ORDERS_PENDING = 'ORDERS_PENDING', _('Commandes en attente')
        ORDER_COMPLETION = 'ORDER_COMPLETION', _('Taux de complétion')
        PRODUCTION_ACTIVE = 'PRODUCTION_ACTIVE', _('Productions actives')
        PRODUCTION_LEAD_TIME = 'PRODUCTION_LEAD_TIME', _('Temps de cycle')
        STOCK_VALUE = 'STOCK_VALUE', _('Valeur stock')
        STOCK_LOW = 'STOCK_LOW', _('Articles en rupture')
        RESOURCE_UTIL = 'RESOURCE_UTIL', _('Taux utilisation ressources')
    
    metric_type = models.CharField(
        max_length=50,
        choices=MetricType.choices,
        verbose_name=_('Type de métrique'),
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
        help_text=_('ex: CFA, %, count, days')
    )
    
    captured_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Capturé le'),
        db_index=True
    )
    
    metadata = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_('Métadonnées'),
        help_text=_('Additional context as JSON')
    )

    class Meta:
        verbose_name = _('Snapshot KPI')
        verbose_name_plural = _('Snapshots KPI')
        ordering = ['-captured_at']
        indexes = [
            models.Index(fields=['metric_type', '-captured_at']),
        ]

    def __str__(self):
        return f"{self.get_metric_type_display()} - {self.metric_value} {self.unit}"


class KPIDashboardConfig(models.Model):
    """
    Customize which KPIs are visible to each user role.
    Allows different views for Admin, Secretary, Production Manager, etc.
    """
    
    class UserRole(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrateur')
        SECRETARY = 'SECRETARY', _('Secrétaire')
        STOCK_MANAGER = 'STOCK_MANAGER', _('Gestionnaire Stock')
        PRODUCTION_MANAGER = 'PRODUCTION_MANAGER', _('Responsable Production')
        TECHNICIAN = 'TECHNICIAN', _('Technicien')
    
    user_role = models.CharField(
        max_length=50,
        choices=UserRole.choices,
        unique=True,
        verbose_name=_('Rôle utilisateur')
    )
    
    # Metric visibility flags
    show_revenue = models.BooleanField(default=True, verbose_name=_('Afficher revenu'))
    show_orders = models.BooleanField(default=True, verbose_name=_('Afficher commandes'))
    show_production = models.BooleanField(default=True, verbose_name=_('Afficher production'))
    show_stock = models.BooleanField(default=True, verbose_name=_('Afficher stock'))
    show_resources = models.BooleanField(default=True, verbose_name=_('Afficher ressources'))
    
    # Chart preferences
    default_chart_type = models.CharField(
        max_length=20,
        choices=[('line', 'Line'), ('bar', 'Bar'), ('pie', 'Pie')],
        default='line',
        verbose_name=_('Type de graphique par défaut')
    )
    
    refresh_interval_minutes = models.PositiveIntegerField(
        default=15,
        verbose_name=_('Intervalle de rafraîchissement (minutes)')
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Créé le'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Mis à jour le'))

    class Meta:
        verbose_name = _('Configuration KPI Dashboard')
        verbose_name_plural = _('Configurations KPI Dashboard')

    def __str__(self):
        return f"KPI Config - {self.get_user_role_display()}"
