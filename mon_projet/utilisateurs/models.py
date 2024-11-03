from django.db import models

class Utilisateur(models.Model):
    nom = models.CharField(max_length=50)
    mot_de_passe = models.CharField(max_length=5000)
    email = models.EmailField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/')
    telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=100)
    sexe = models.CharField(max_length=20)

    def __str__(self):
        return self.email
