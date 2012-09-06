from django import forms
from django.utils.translation import ugettext_lazy as _

from mptt.forms import TreeNodeChoiceField

from models import Category, Product

class CategoryForm(forms.ModelForm):

    parent = TreeNodeChoiceField(   queryset=Category.tree.all(),
                                    level_indicator=3*unichr(160),
                                    empty_label='---------',
                                    required=False)

    class Meta:
        model = Category

class ProductForm(forms.ModelForm):

    category = TreeNodeChoiceField( queryset=Category.tree.all(),
                                    level_indicator=3*unichr(160),
                                    empty_label='---------',
                                    required=True)

    class Meta:
        model = Product
