from django import forms
from mptt.forms import TreeNodeChoiceField
from models import Category

class CategoryForm(forms.ModelForm):
    
    parent = TreeNodeChoiceField(queryset=Category.tree.all(), level_indicator=3*unichr(160), empty_label='---------', required=False)
    
    class Meta:
        model = Category
        