from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.users.mixins import AdminOrSecretaryMixin, AllStaffMixin
from .models import Commande
from .forms import CommandeForm


class CommandeListView(AllStaffMixin, ListView):
    model = Commande
    template_name = 'commandes/commande_list.html'
    context_object_name = 'commandes'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('client').order_by('-order_date')
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')
        if search:
            queryset = queryset.filter(order_number__icontains=search) | queryset.filter(client__name__icontains=search)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['statuses'] = Commande.Status.choices
        return context


class CommandeDetailView(AllStaffMixin, DetailView):
    model = Commande
    template_name = 'commandes/commande_detail.html'
    context_object_name = 'commande'

    def get_queryset(self):
        return super().get_queryset().select_related('client')


class CommandeCreateView(AdminOrSecretaryMixin, CreateView):
    model = Commande
    form_class = CommandeForm
    template_name = 'commandes/commande_form.html'
    success_url = reverse_lazy('commandes:commande_list')

    def form_valid(self, form):
        messages.success(self.request, 'Commande créée avec succès.')
        return super().form_valid(form)


class CommandeUpdateView(AdminOrSecretaryMixin, UpdateView):
    model = Commande
    form_class = CommandeForm
    template_name = 'commandes/commande_form.html'
    success_url = reverse_lazy('commandes:commande_list')

    def form_valid(self, form):
        messages.success(self.request, 'Commande modifiée avec succès.')
        return super().form_valid(form)


class CommandeDeleteView(AdminOrSecretaryMixin, DeleteView):
    model = Commande
    template_name = 'commandes/commande_confirm_delete.html'
    success_url = reverse_lazy('commandes:commande_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Commande supprimée.')
        return super().delete(request, *args, **kwargs)
