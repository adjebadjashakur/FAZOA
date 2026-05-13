from django.contrib import admin
from .models import Report, ReportLine


class ReportLineInline(admin.TabularInline):
    model = ReportLine
    extra = 1
    readonly_fields = ['created_at']
    fields = ['metric_name', 'metric_value', 'unit', 'created_at']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'start_date', 'end_date', 'generated_by', 'generated_at']
    list_filter = ['report_type', 'generated_at']
    search_fields = ['name', 'generated_by']
    ordering = ['-generated_at']
    readonly_fields = ['generated_at']
    inlines = [ReportLineInline]

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


@admin.register(ReportLine)
class ReportLineAdmin(admin.ModelAdmin):
    list_display = ['metric_name', 'metric_value', 'unit', 'report', 'created_at']
    list_filter = ['report__report_type', 'created_at']
    search_fields = ['metric_name', 'report__name']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
