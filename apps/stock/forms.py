from django import forms
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
