from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'start_date', 'end_date', 'generated_by', 'generated_at']
    list_filter = ['report_type', 'generated_at']
    search_fields = ['name', 'generated_by']
    ordering = ['-generated_at']
    readonly_fields = ['generated_at']

    fieldsets = [
        ('Informations du rapport', {
            'fields': ['name', 'report_type', 'description']
        }),
        ('Période', {
            'fields': ['start_date', 'end_date']
        }),
        ('Génération', {
            'fields': ['generated_by', 'generated_at', 'data']
        }),
    ]
    