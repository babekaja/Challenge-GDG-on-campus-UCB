from django import forms
from .models import Utilisateur
from django.contrib.auth.hashers import make_password

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['email', 'mot_de_passe']
        widgets = {
            'mot_de_passe': forms.PasswordInput(attrs={'placeholder': 'password'})
        }

    def clean_mot_de_passe(self):
        mot_de_passe = self.cleaned_data.get('mot_de_passe')
        if len(mot_de_passe) < 8:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return mot_de_passe

    def save(self, commit=True):
        utilisateur = super().save(commit=False)
        # Hasher le mot de passe avant de l'enregistrer
        utilisateur.mot_de_passe = make_password(self.cleaned_data['mot_de_passe'])
        if commit:
            utilisateur.save()
        return utilisateur


class ConnexionForm(forms.Form):
    email = forms.EmailField(max_length=100, label="Adresse email")
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Entrez votre mot de passe'}),
                                   label="Mot de passe")
from django import forms
from .models import Utilisateur

class ModificationForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'email', 'telephone', 'adresse', 'sexe', 'image']  # Ajoutez les champs souhaités
        widgets = {
            'sexe': forms.Select(choices=[('M', 'Masculin'), ('F', 'Féminin')]),  # Exemple de sélection pour sexe
        }
