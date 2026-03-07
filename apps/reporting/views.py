from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.users.mixins import AllStaffMixin, AdminRequiredMixin
from .models import Report
from .forms import ReportForm


class ReportListView(AllStaffMixin, ListView):
    model = Report
    template_name = 'reporting/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-generated_at')
        report_type = self.request.GET.get('type', '')
        if report_type:
            queryset = queryset.filter(report_type=report_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_type'] = self.request.GET.get('type', '')
        context['types'] = Report.ReportType.choices
        return context


class ReportDetailView(AllStaffMixin, DetailView):
    model = Report
    template_name = 'reporting/report_detail.html'
    context_object_name = 'report'


class ReportCreateView(AdminRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reporting/report_form.html'
    success_url = reverse_lazy('reporting:report_list')

    def form_valid(self, form):
        messages.success(self.request, 'Rapport créé avec succès.')
        return super().form_valid(form)


class ReportUpdateView(AdminRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reporting/report_form.html'
    success_url = reverse_lazy('reporting:report_list')

    def form_valid(self, form):
        messages.success(self.request, 'Rapport modifié avec succès.')
        return super().form_valid(form)


class ReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    template_name = 'reporting/report_confirm_delete.html'
    success_url = reverse_lazy('reporting:report_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Rapport supprimé.')
        return super().delete(request, *args, **kwargs)
