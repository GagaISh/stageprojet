from django import forms
from .models import CustomUser

class InscriptionForm(forms.ModelForm):

    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["nom", "prenom", "date_naissance", "telephone", "adresse", "email", "password1", "password2"]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }
        required = ['date_naissance']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    class ConnexionForm(forms.Form):
     email = forms.EmailField(label='Adresse e-mail')
     mot_de_passe = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

