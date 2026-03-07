from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.users.models import User
from apps.clients.models import Client
from apps.commandes.models import Commande
from apps.stock.models import Stock
from apps.production.models import Production
from apps.ressources.models import Ressource
from apps.reporting.models import Report


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['user_role'] = user.get_role_display()

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
                .order_by('-id')[:5]
            )

        return context
