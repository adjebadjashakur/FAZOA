"""
KPI Calculation Service Layer

Provides business logic for calculating key performance indicators
across Orders, Production, Stock, and Resources.
"""

from django.db.models import (
    Q, F, Sum, Count, Avg, Case, When, DecimalField, IntegerField, 
    Prefetch, Value, ExpressionWrapper, DurationField, Max, Min
)
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from apps.commandes.models import Commande
from apps.production.models import Production
from apps.stock.models import Stock, StockMovement
from apps.ressources.models import Ressource


class OrderMetrics:
    """Calculate order and revenue-related KPIs."""
    
    @staticmethod
    def get_total_revenue():
        """Total revenue from all confirmed orders."""
        return (
            Commande.objects
            .filter(status__in=['CONFIRMED', 'IN_PRODUCTION', 'COMPLETED'])
            .aggregate(
                total=Sum(
                    ExpressionWrapper(
                        F('quantity') * F('unit_price'),
                        output_field=DecimalField()
                    )
                )
            )['total'] or Decimal('0.00')
        )
    
    @staticmethod
    def get_pending_orders_count():
        """Count of orders awaiting confirmation."""
        return Commande.objects.filter(status='PENDING').count()
    
    @staticmethod
    def get_completion_rate():
        """Percentage of completed orders."""
        total = Commande.objects.count()
        if total == 0:
            return Decimal('0.00')
        completed = Commande.objects.filter(status='COMPLETED').count()
        return Decimal(completed * 100 / total)
    
    @staticmethod
    def get_average_order_value():
        """Average value per order."""
        stats = Commande.objects.aggregate(
            avg_value=Avg(
                ExpressionWrapper(
                    F('quantity') * F('unit_price'),
                    output_field=DecimalField()
                )
            )
        )
        return stats['avg_value'] or Decimal('0.00')
    
    @staticmethod
    def get_revenue_by_status():
        """Revenue breakdown by order status."""
        return (
            Commande.objects
            .values('status')
            .annotate(
                count=Count('id'),
                revenue=Sum(
                    ExpressionWrapper(
                        F('quantity') * F('unit_price'),
                        output_field=DecimalField()
                    )
                )
            )
            .order_by('-revenue')
        )
    
    @staticmethod
    def get_monthly_revenue(months=12):
        """Revenue trend for the last N months."""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30*months)
        
        return (
            Commande.objects
            .filter(order_date__gte=start_date)
            .extra(
                select={'month': 'DATE_TRUNC(\'month\', order_date)'}
            )
            .values('month')
            .annotate(
                revenue=Sum(
                    ExpressionWrapper(
                        F('quantity') * F('unit_price'),
                        output_field=DecimalField()
                    )
                ),
                count=Count('id')
            )
            .order_by('month')
        )


class ProductionMetrics:
    """Calculate production-related KPIs."""
    
    @staticmethod
    def get_active_productions_count():
        """Count of productions currently in progress."""
        return Production.objects.filter(status='IN_PROGRESS').count()
    
    @staticmethod
    def get_production_status_distribution():
        """Count of productions by status."""
        return (
            Production.objects
            .values('status')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
    
    @staticmethod
    def get_average_lead_time():
        """Average days from order to completion."""
        completions = (
            Production.objects
            .filter(status='COMPLETED')
            .annotate(
                lead_days=ExpressionWrapper(
                    (F('end_date') - F('commande__order_date')),
                    output_field=DurationField()
                )
            )
            .aggregate(
                avg_days=Avg(
                    ExpressionWrapper(
                        (F('end_date') - F('commande__order_date')) / 
                        timedelta(days=1),
                        output_field=DecimalField()
                    )
                )
            )
        )
        return completions['avg_days'] or Decimal('0.00')
    
    @staticmethod
    def get_on_time_delivery_rate():
        """Percentage of orders completed by expected delivery date."""
        total_completed = Production.objects.filter(status='COMPLETED').count()
        if total_completed == 0:
            return Decimal('0.00')
        
        on_time = Production.objects.filter(
            status='COMPLETED',
            end_date__lte=F('commande__expected_delivery')
        ).count()
        
        return Decimal(on_time * 100 / total_completed)
    
    @staticmethod
    def get_production_by_status():
        """Detailed breakdown by production status."""
        return (
            Production.objects
            .values('status')
            .annotate(
                count=Count('id'),
                avg_progress=Avg('progress_percentage')
            )
            .order_by('-count')
        )


class StockMetrics:
    """Calculate inventory-related KPIs."""
    
    @staticmethod
    def get_total_stock_value():
        """Total value of all inventory."""
        return (
            Stock.objects
            .aggregate(
                total=Sum(
                    ExpressionWrapper(
                        F('quantity') * F('unit_price'),
                        output_field=DecimalField()
                    )
                )
            )['total'] or Decimal('0.00')
        )
    
    @staticmethod
    def get_low_stock_count():
        """Count of items below minimum quantity."""
        return (
            Stock.objects
            .filter(quantity__lt=F('minimum_quantity'))
            .count()
        )
    
    @staticmethod
    def get_stock_by_category():
        """Stock distribution by category."""
        return (
            Stock.objects
            .values('category')
            .annotate(
                count=Count('id'),
                total_value=Sum(
                    ExpressionWrapper(
                        F('quantity') * F('unit_price'),
                        output_field=DecimalField()
                    )
                ),
                avg_quantity=Avg('quantity')
            )
            .order_by('-total_value')
        )
    
    @staticmethod
    def get_inventory_turnover():
        """Average number of times inventory is sold and replaced."""
        stock_count = Stock.objects.count()
        if stock_count == 0:
            return Decimal('0.00')
        
        movement_stats = (
            StockMovement.objects
            .filter(movement_type='SORTIE')
            .values('stock_id')
            .annotate(total_out=Sum('quantity_changed'))
            .aggregate(avg_turnover=Avg('total_out'))
        )
        
        return movement_stats['avg_turnover'] or Decimal('0.00')
    
    @staticmethod
    def get_slow_moving_items(threshold_days=90):
        """Items with no outbound movement in N days."""
        cutoff_date = timezone.now() - timedelta(days=threshold_days)
        
        return (
            Stock.objects
            .exclude(
                movements__movement_type='SORTIE',
                movements__created_at__gte=cutoff_date
            )
            .values('id', 'sku', 'name', 'quantity', 'unit_price')
            .annotate(
                stock_value=ExpressionWrapper(
                    F('quantity') * F('unit_price'),
                    output_field=DecimalField()
                )
            )
        )
    
    @staticmethod
    def get_restock_alerts():
        """Items needing urgent reordering."""
        return (
            Stock.objects
            .filter(quantity__lte=F('minimum_quantity'))
            .values('id', 'sku', 'name', 'quantity', 'minimum_quantity')
            .order_by('quantity')
        )


class ResourceMetrics:
    """Calculate resource utilization KPIs."""
    
    @staticmethod
    def get_total_resources():
        """Total count of resources by type."""
        return (
            Ressource.objects
            .values('resource_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
    
    @staticmethod
    def get_available_resources():
        """Count of available (not in use) resources."""
        return (
            Ressource.objects
            .filter(is_available=True)
            .values('resource_type')
            .annotate(count=Count('id'))
        )
    
    @staticmethod
    def get_resource_utilization_rate():
        """Percentage of resources currently in use."""
        total = Ressource.objects.count()
        if total == 0:
            return Decimal('0.00')
        
        in_use = Ressource.objects.filter(is_available=False).count()
        return Decimal(in_use * 100 / total)
    
    @staticmethod
    def get_resource_allocation():
        """Detailed resource allocation by type."""
        return (
            Ressource.objects
            .values('resource_type')
            .annotate(
                total=Count('id'),
                available=Count('id', filter=Q(is_available=True)),
                in_use=Count('id', filter=Q(is_available=False))
            )
            .order_by('resource_type')
        )


class DashboardKPIs:
    """Aggregated KPI service for dashboard rendering."""
    
    @staticmethod
    def get_all_kpis():
        """Get all KPIs for dashboard display."""
        return {
            'orders': {
                'total_revenue': str(OrderMetrics.get_total_revenue()),
                'pending_count': OrderMetrics.get_pending_orders_count(),
                'completion_rate': str(OrderMetrics.get_completion_rate()),
                'average_order_value': str(OrderMetrics.get_average_order_value()),
                'revenue_by_status': list(OrderMetrics.get_revenue_by_status()),
                'monthly_revenue': list(OrderMetrics.get_monthly_revenue()),
            },
            'production': {
                'active_count': ProductionMetrics.get_active_productions_count(),
                'status_distribution': list(ProductionMetrics.get_production_status_distribution()),
                'avg_lead_time': str(ProductionMetrics.get_average_lead_time()),
                'on_time_rate': str(ProductionMetrics.get_on_time_delivery_rate()),
                'by_status': list(ProductionMetrics.get_production_by_status()),
            },
            'stock': {
                'total_value': str(StockMetrics.get_total_stock_value()),
                'low_stock_count': StockMetrics.get_low_stock_count(),
                'by_category': list(StockMetrics.get_stock_by_category()),
                'turnover_rate': str(StockMetrics.get_inventory_turnover()),
                'restock_alerts': list(StockMetrics.get_restock_alerts()),
                'slow_moving': list(StockMetrics.get_slow_moving_items()),
            },
            'resources': {
                'total_by_type': list(ResourceMetrics.get_total_resources()),
                'available_count': list(ResourceMetrics.get_available_resources()),
                'utilization_rate': str(ResourceMetrics.get_resource_utilization_rate()),
                'allocation': list(ResourceMetrics.get_resource_allocation()),
            },
        }
