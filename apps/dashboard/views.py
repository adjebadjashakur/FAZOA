from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.users.models import User
from apps.clients.models import Client
from apps.commandes.models import Commande
from apps.stock.models import Stock
from apps.production.models import Production
from apps.ressources.models import Ressource
from apps.reporting.models import Report
from .services import DashboardKPIs, OrderMetrics, ProductionMetrics, StockMetrics, ResourceMetrics


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['user_role'] = user.get_role_display()
        
        # Load all KPIs (filtered based on role below)
        all_kpis = DashboardKPIs.get_all_kpis()
        context['kpis'] = all_kpis

        # ✅ Statistiques globales — order_by() vide annule tout ordering par défaut
        context['total_users']       = User.objects.order_by().count()
        context['total_clients']     = Client.objects.order_by().count()
        context['total_commandes']   = Commande.objects.order_by().count()
        context['total_stock_items'] = Stock.objects.order_by().count()
        context['total_productions'] = Production.objects.order_by().count()
        context['total_ressources']  = Ressource.objects.order_by().count()

        # ✅ Dashboard Admin
        if user.is_superuser or user.role == 'ADMIN':
            context['is_admin'] = True
            context['pending_orders'] = (
                Commande.objects
                .filter(status='PENDING')
                .order_by()
                .count()
            )
            # order_date est le vrai champ du modèle Commande
            context['recent_orders'] = (
                Commande.objects
                .select_related('client')
                .order_by('-order_date')[:5]
            )
            context['total_reports'] = Report.objects.order_by().count()
            
            # Add KPI specific to admin
            context['admin_kpis'] = {
                'total_revenue': all_kpis['orders']['total_revenue'],
                'completion_rate': all_kpis['orders']['completion_rate'],
                'production_active': all_kpis['production']['active_count'],
                'on_time_rate': all_kpis['production']['on_time_rate'],
                'stock_value': all_kpis['stock']['total_value'],
                'low_stock_alerts': all_kpis['stock']['restock_alerts'],
                'resource_util': all_kpis['resources']['utilization_rate'],
            }

        # ✅ Dashboard Secrétaire
        elif user.role == 'SECRETARY':
            context['is_secretary'] = True
            context['pending_orders'] = (
                Commande.objects
                .filter(status='PENDING')
                .order_by()
                .count()
            )
            context['recent_orders'] = (
                Commande.objects
                .select_related('client')
                .order_by('-order_date')[:5]
            )

        # ✅ Dashboard Gestionnaire Stock
        elif user.role == 'STOCK_MANAGER':
            context['is_stock_manager'] = True
            # Adapte le seuil (10) et le champ quantity à ton modèle réel
            context['low_stock_items'] = (
                Stock.objects
                .filter(quantity__lt=10)
                .order_by()
                .count()
            )
            context['recent_stock'] = (
                Stock.objects
                .order_by('quantity')[:5]  # les plus faibles en stock en premier
            )
            
            # Add KPI specific to stock manager
            context['stock_kpis'] = {
                'total_value': all_kpis['stock']['total_value'],
                'low_stock_count': all_kpis['stock']['low_stock_count'],
                'turnover_rate': all_kpis['stock']['turnover_rate'],
                'by_category': all_kpis['stock']['by_category'],
                'restock_alerts': all_kpis['stock']['restock_alerts'][:10],
                'slow_moving': all_kpis['stock']['slow_moving'][:5],
            }

        # ✅ Dashboard Responsable Production
        elif user.role == 'PRODUCTION_MANAGER':
            context['is_production_manager'] = True
            # Vérifie que 'IN_PROGRESS' correspond bien aux choices de ton modèle Production
            context['active_productions'] = (
                Production.objects
                .filter(status='IN_PROGRESS')
                .order_by()
                .count()
            )
            context['recent_productions'] = (
                Production.objects
                .select_related('commande')
                .order_by('-id')[:5]
            )
            
            # Add KPI specific to production manager
            context['production_kpis'] = {
                'active_count': all_kpis['production']['active_count'],
                'avg_lead_time': all_kpis['production']['avg_lead_time'],
                'on_time_rate': all_kpis['production']['on_time_rate'],
                'status_distribution': all_kpis['production']['status_distribution'],
                'by_status': all_kpis['production']['by_status'],
            }

        return context
