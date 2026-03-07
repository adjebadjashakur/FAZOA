from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.users.mixins import AdminOrProductionMixin, AllStaffMixin
from .models import Production
from .forms import ProductionForm


class ProductionListView(AllStaffMixin, ListView):
    model = Production
    template_name = 'production/production_list.html'
    context_object_name = 'productions'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status', '')
        context['statuses'] = Production.Status.choices
        return context


class ProductionDetailView(AllStaffMixin, DetailView):
    model = Production
    template_name = 'production/production_detail.html'
    context_object_name = 'production'


class ProductionCreateView(AdminOrProductionMixin, CreateView):
    model = Production
    form_class = ProductionForm
    template_name = 'production/production_form.html'
    success_url = reverse_lazy('production:production_list')

    def form_valid(self, form):
        messages.success(self.request, 'Production créée avec succès.')
        return super().form_valid(form)


class ProductionUpdateView(AdminOrProductionMixin, UpdateView):
    model = Production
    form_class = ProductionForm
    template_name = 'production/production_form.html'
    success_url = reverse_lazy('production:production_list')

    def form_valid(self, form):
        messages.success(self.request, 'Production modifiée avec succès.')
        return super().form_valid(form)


class ProductionDeleteView(AdminOrProductionMixin, DeleteView):
    model = Production
    template_name = 'production/production_confirm_delete.html'
    success_url = reverse_lazy('production:production_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Production supprimée.')
        return super().delete(request, *args, **kwargs)
