from django import forms

from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm the Password", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = [
            "last_name",
            "first_name",
            "birth_date",
            "telephone",
            "address",
            "email",
            "password1",
            "password2",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }
        required = ["birth_date"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Password do not match."))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class LoginForm(forms.Form):
        email = forms.EmailField(label="e-mail")
        password = forms.CharField(label="password", widget=forms.PasswordInput)
