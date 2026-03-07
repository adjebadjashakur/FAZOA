from django import forms
from .models import Ressource


class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ['name', 'description', 'resource_type', 'status', 'location', 'capacity', 'acquisition_date', 'maintenance_date', 'cost', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
