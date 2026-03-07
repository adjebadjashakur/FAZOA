from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.users.mixins import AllStaffMixin, AdminRequiredMixin
from .models import Ressource
from .forms import RessourceForm


class RessourceListView(AllStaffMixin, ListView):
    model = Ressource
    template_name = 'ressources/ressource_list.html'
    context_object_name = 'ressources'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        search = self.request.GET.get('search', '')
        resource_type = self.request.GET.get('type', '')
        if search:
            queryset = queryset.filter(name__icontains=search)
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['resource_type'] = self.request.GET.get('type', '')
        context['types'] = Ressource.Type.choices
        return context


class RessourceDetailView(AllStaffMixin, DetailView):
    model = Ressource
    template_name = 'ressources/ressource_detail.html'
    context_object_name = 'ressource'


class RessourceCreateView(AdminRequiredMixin, CreateView):
    model = Ressource
    form_class = RessourceForm
    template_name = 'ressources/ressource_form.html'
    success_url = reverse_lazy('ressources:ressource_list')

    def form_valid(self, form):
        messages.success(self.request, 'Ressource créée avec succès.')
        return super().form_valid(form)


class RessourceUpdateView(AdminRequiredMixin, UpdateView):
    model = Ressource
    form_class = RessourceForm
    template_name = 'ressources/ressource_form.html'
    success_url = reverse_lazy('ressources:ressource_list')

    def form_valid(self, form):
        messages.success(self.request, 'Ressource modifiée avec succès.')
        return super().form_valid(form)


class RessourceDeleteView(AdminRequiredMixin, DeleteView):
    model = Ressource
    template_name = 'ressources/ressource_confirm_delete.html'
    success_url = reverse_lazy('ressources:ressource_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Ressource supprimée.')
        return super().delete(request, *args, **kwargs)
