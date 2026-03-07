from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.users.mixins import AdminOrSecretaryMixin, AllStaffMixin
from .models import Client
from .forms import ClientForm


class ClientListView(AllStaffMixin, ListView):
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-registration_date')
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(email__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class ClientDetailView(AllStaffMixin, DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'


class ClientCreateView(AdminOrSecretaryMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')

    def form_valid(self, form):
        messages.success(self.request, 'Client créé avec succès.')
        return super().form_valid(form)


class ClientUpdateView(AdminOrSecretaryMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')

    def form_valid(self, form):
        messages.success(self.request, 'Client modifié avec succès.')
        return super().form_valid(form)


class ClientDeleteView(AdminOrSecretaryMixin, DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('clients:client_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Client supprimé.')
        return super().delete(request, *args, **kwargs)
