from django import forms
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class UserForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'required': 'required',
            })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'required': 'required',
            })
    )

    class Meta:
        model = UserModel
        fields = (
            'first_name',
            'last_name',
        )
