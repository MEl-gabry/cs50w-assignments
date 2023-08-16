from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

class EditPageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))