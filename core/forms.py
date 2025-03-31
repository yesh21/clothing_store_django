from django import forms
from .models import Product


class ProductFilterForm(forms.Form):
    category = forms.ChoiceField(choices=[("", "All")] + Product.CATEGORY_CHOICES)
    # size = forms.ChoiceField(choices=[("", "All")] + Product.SIZE_CHOICES)
    color = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False, decimal_places=2)
    max_price = forms.DecimalField(required=False, decimal_places=2)
