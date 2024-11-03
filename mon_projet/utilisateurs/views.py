from django.shortcuts import render, redirect , redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .forms import InscriptionForm, ConnexionForm, ModificationForm 
from .models import Utilisateur
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Utilisateur
import openpyxl
from django.http import HttpResponse

def export_excel(request):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="utilisateurs.xlsx"'

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Utilisateurs'

    # En-têtes du tableau
    headers = ['Nom', 'Email', 'Téléphone', 'Adresse', 'Sexe']
    sheet.append(headers)

    utilisateurs = Utilisateur.objects.all()
    for utilisateur in utilisateurs:
        sheet.append([utilisateur.nom, utilisateur.email, utilisateur.telephone,
                      utilisateur.adresse, utilisateur.sexe])

    workbook.save(response)
    return response


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="utilisateurs.pdf"'
    p = canvas.Canvas(response, pagesize=letter)

    utilisateurs = Utilisateur.objects.all()
    y = 750

    p.drawString(200, 800, "Liste des Utilisateurs")
    p.line(30, 780, 580, 780)

    for utilisateur in utilisateurs:
        p.drawString(30, y, f"Nom : {utilisateur.nom}")
        p.drawString(200, y, f"Email : {utilisateur.email}")
        p.drawString(350, y, f"Téléphone : {utilisateur.telephone}")
        p.drawString(450, y, f"Adresse : {utilisateur.adresse}")
        p.drawString(500, y, f"Sexe : {utilisateur.sexe}")
        y -= 20

        if y < 50:  # Nouvelle page si l'espace est insuffisant
            p.showPage()
            y = 750

    p.save()
    return response


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistre l'utilisateur avec le mot de passe hashé
            messages.success(request, "Inscription réussie. Vous pouvez maintenant vous connecter.")
            return redirect('connexion')
        else:
            messages.error(request, "Erreur dans l'inscription. Veuillez vérifier vos informations.")
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            mot_de_passe = form.cleaned_data.get('mot_de_passe')
            try:
                utilisateur = Utilisateur.objects.get(email=email)
                if check_password(mot_de_passe, utilisateur.mot_de_passe):
                    # Enregistre l'ID utilisateur dans la session
                    request.session['utilisateur_id'] = utilisateur.id
                    messages.success(request, "Connexion réussie.")
                    # Redirige vers la page du tableau de bord
                    return redirect('tableau_de_bord')
                else:
                    messages.error(request, "Mot de passe incorrect.")
            except Utilisateur.DoesNotExist:
                messages.error(request, "Utilisateur non trouvé.")
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier vos informations.")
    else:
        form = ConnexionForm()
    return render(request, 'connexion.html', {'form': form})

def tableau_de_bord(request):
    utilisateur_id = request.session.get('utilisateur_id')
    if utilisateur_id:
        utilisateur = Utilisateur.objects.get(id=utilisateur_id)
        return render(request, 'tableau_de_bord.html', {'utilisateur': utilisateur})
    return redirect('connexion')

def deconnexion(request):
    request.session.flush()
    return redirect('connexion')

def modifier_profil(request, utilisateur_id):
    utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id)

    if request.method == 'POST':
        form = ModificationForm(request.POST, request.FILES, instance=utilisateur)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informations mises à jour avec succès.')
            return redirect('tableau_de_bord')  # Redirige vers la page du tableau de bord
        else:
            messages.error(request, 'Erreur dans le formulaire. Veuillez vérifier vos informations.')
    else:
        form = ModificationForm(instance=utilisateur)

    return render(request, 'modifier_profil.html', {'form': form, 'utilisateur': utilisateur})


def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()  # Récupérer tous les utilisateurs
    return render(request, 'liste_utilisateurs.html', {'utilisateurs': utilisateurs})
