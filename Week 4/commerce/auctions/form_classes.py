from django import forms
from django.forms.widgets import Textarea

from auctions.models import Category


class NewListingForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),max_length=20)
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), max_length=1000)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    image = forms.URLField(required=False)