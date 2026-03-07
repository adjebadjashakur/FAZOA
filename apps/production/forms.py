from django import forms
from .models import Production


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['commande', 'start_date', 'status', 'produced_quantity', 'defective_quantity', 'quality_notes', 'assigned_team', 'line_number', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
