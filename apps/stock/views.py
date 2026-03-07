from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.users.mixins import AdminOrStockMixin, AllStaffMixin
from .models import Stock
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
