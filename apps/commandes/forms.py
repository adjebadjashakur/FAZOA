from django import forms
from django.core.exceptions import ValidationError
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

    def clean(self):
        super().clean()
        quantity = self.cleaned_data.get('quantity')
        unit_price = self.cleaned_data.get('unit_price')
        total_price = self.cleaned_data.get('total_price')
        
        # Validate total_price = quantity × unit_price
        if quantity and unit_price and total_price:
            expected_total = quantity * unit_price
            if abs(total_price - expected_total) > 0.01:
                raise ValidationError('Prix total ne correspond pas à Quantité × Prix unitaire')
