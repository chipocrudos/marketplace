from django import forms
from ..models import Job
from datetime import date


class JobForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-4',
                'autocomplete': 'off',
                'required': 'required',
            })
    )
    budget = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'number',
                'autocomplete': 'off',
                'required': 'required',
                'min': 0.00,
                'step': 0.01
            })
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control md-textarea',
                'autocomplete': 'off',
                'required': 'required',
            })
    )
    expired = forms.DateField(
        initial=date.today,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'autocomplete': 'off',
                'required': 'required',
            }),
        help_text='Expiration day'
    )

    class Meta:
        model = Job
        fields = (
            'title',
            'description',
            'budget',
            'expired'
        )

    def clean_expired(self):
        expired = self.cleaned_data.get('expired')
        print(expired)
        if expired < date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return expired
