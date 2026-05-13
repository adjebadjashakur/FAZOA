from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
import csv
from apps.users.mixins import AdminOrStockMixin, AllStaffMixin
from .models import Stock, StockMovement
from .forms import StockForm


class StockListView(AllStaffMixin, ListView):
    model = Stock
    template_name = 'stock/stock_list.html'
    context_object_name = 'stocks'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        search = self.request.GET.get('search', '')
        low_stock = self.request.GET.get('low_stock', False)
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(sku__icontains=search)
        if low_stock:
            queryset = queryset.filter(quantity__lte=10)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['low_stock'] = self.request.GET.get('low_stock', False)
        return context


class StockDetailView(AllStaffMixin, DetailView):
    model = Stock
    template_name = 'stock/stock_detail.html'
    context_object_name = 'stock'


class StockCreateView(AdminOrStockMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = 'stock/stock_form.html'
    success_url = reverse_lazy('stock:stock_list')

    def form_valid(self, form):
        messages.success(self.request, 'Article de stock créé avec succès.')
        return super().form_valid(form)


class StockUpdateView(AdminOrStockMixin, UpdateView):
    model = Stock
    form_class = StockForm
    template_name = 'stock/stock_form.html'
    success_url = reverse_lazy('stock:stock_list')

    def form_valid(self, form):
        messages.success(self.request, 'Article de stock modifié avec succès.')
        return super().form_valid(form)


class StockDeleteView(AdminOrStockMixin, DeleteView):
    model = Stock
    template_name = 'stock/stock_confirm_delete.html'
    success_url = reverse_lazy('stock:stock_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Article de stock supprimé.')
        return super().delete(request, *args, **kwargs)


# ============================================================================
# STOCK MOVEMENT VIEWS (BLOCK 4)
# ============================================================================

class StockMovementListView(AllStaffMixin, ListView):
    """List all stock movements with filtering and search."""
    model = StockMovement
    template_name = 'stock/movement_list.html'
    context_object_name = 'movements'
    paginate_by = 50

    def get_queryset(self):
        queryset = (
            super().get_queryset()
            .select_related('stock', 'created_by')
            .order_by('-created_at')
        )
        
        # Filters
        movement_type = self.request.GET.get('movement_type', '')
        stock_id = self.request.GET.get('stock_id', '')
        user_id = self.request.GET.get('user_id', '')
        days = self.request.GET.get('days', '')
        search = self.request.GET.get('search', '')
        
        if movement_type:
            queryset = queryset.filter(movement_type=movement_type)
        if stock_id:
            queryset = queryset.filter(stock_id=stock_id)
        if user_id:
            queryset = queryset.filter(created_by_id=user_id)
        if days:
            try:
                days_int = int(days)
                cutoff = timezone.now() - timedelta(days=days_int)
                queryset = queryset.filter(created_at__gte=cutoff)
            except ValueError:
                pass
        if search:
            queryset = queryset.filter(
                Q(stock__sku__icontains=search) |
                Q(stock__name__icontains=search) |
                Q(reason__icontains=search)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movement_types'] = StockMovement.MovementType.choices
        context['selected_type'] = self.request.GET.get('movement_type', '')
        context['selected_days'] = self.request.GET.get('days', '')
        context['search'] = self.request.GET.get('search', '')
        return context


class StockMovementDetailView(AllStaffMixin, DetailView):
    """View detailed information about a specific stock movement."""
    model = StockMovement
    template_name = 'stock/movement_detail.html'
    context_object_name = 'movement'

    def get_queryset(self):
        return super().get_queryset().select_related('stock', 'created_by')


class StockMovementHistoryView(AllStaffMixin, DetailView):
    """Display timeline of all movements for a specific stock item."""
    model = Stock
    template_name = 'stock/movement_history.html'
    context_object_name = 'stock'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = self.get_object()
        
        # Get movement timeline
        context['movements'] = (
            stock.movements
            .select_related('created_by')
            .order_by('-created_at')
        )
        
        # Summary stats
        context['total_movements'] = context['movements'].count()
        context['entries'] = context['movements'].filter(movement_type='ENTREE').count()
        context['exits'] = context['movements'].filter(movement_type='SORTIE').count()
        context['adjustments'] = context['movements'].filter(movement_type='AJUSTEMENT').count()
        
        return context


class StockMovementExportView(AdminOrStockMixin, TemplateView):
    """Export stock movements to CSV."""
    
    def get(self, request, *args, **kwargs):
        # Get filtered movements
        movements = (
            StockMovement.objects
            .select_related('stock', 'created_by')
            .order_by('-created_at')
        )
        
        # Apply same filters as list view
        movement_type = request.GET.get('movement_type', '')
        stock_id = request.GET.get('stock_id', '')
        days = request.GET.get('days', '')
        
        if movement_type:
            movements = movements.filter(movement_type=movement_type)
        if stock_id:
            movements = movements.filter(stock_id=stock_id)
        if days:
            try:
                days_int = int(days)
                cutoff = timezone.now() - timedelta(days=days_int)
                movements = movements.filter(created_at__gte=cutoff)
            except ValueError:
                pass
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stock_movements.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'SKU', 'Nom', 'Type', 'Quantité avant', 'Quantité après', 
            'Changement', 'Raison', 'Référence', 'Créé par', 'Date'
        ])
        
        for movement in movements:
            writer.writerow([
                movement.stock.sku,
                movement.stock.name,
                movement.get_movement_type_display(),
                movement.quantity_before,
                movement.quantity_after,
                movement.quantity_changed,
                movement.reason,
                f"{movement.reference_type}_{movement.reference_id}" if movement.reference_id else '',
                movement.created_by.get_full_name() if movement.created_by else '',
                movement.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            ])
        
        return response
