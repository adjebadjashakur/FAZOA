from django import forms
from django.core.exceptions import ValidationError
from .models import Stock


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['sku', 'name', 'description', 'category', 'quantity', 'minimum_quantity', 'unit_price', 'supplier', 'location', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            })

    def clean(self):
        super().clean()
        quantity = self.cleaned_data.get('quantity')
        minimum_quantity = self.cleaned_data.get('minimum_quantity')
        
        # Validate quantity >= minimum_quantity
        if quantity is not None and minimum_quantity is not None:
            if quantity < minimum_quantity:
                raise ValidationError('Quantité doit être ≥ quantité minimale')
