from django import forms
from django.utils.translation import ugettext_lazy as _

from mptt.forms import TreeNodeChoiceField

from models import Category, Product

class CategoryForm(forms.ModelForm):

    parent = TreeNodeChoiceField(   verbose_name=_('Parent category'),
                                    queryset=Category.tree.all(),
                                    level_indicator=3*unichr(160),
                                    empty_label='---------',
                                    required=False)

    class Meta:
        model = Category

class ProductForm(forms.ModelForm):

    category = TreeNodeChoiceField( verbose_name=_('Category'),
                                    queryset=Category.tree.all(),
                                    level_indicator=3*unichr(160),
                                    empty_label='---------',
                                    required=True)

    class Meta:
        model = Product
