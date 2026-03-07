from django import forms
from .models import Commande


class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['client', 'order_number', 'description', 'quantity', 'unit_price', 'total_price', 'status', 'expected_delivery', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            })
