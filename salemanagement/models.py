from datetime import timezone
from django.db import models
from django.contrib.auth.models import User 

class Article(models.Model):
    code = models.CharField(max_length=255)
    description = models.TextField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    emplacement = models.ForeignKey('EmplacementArticle', on_delete=models.CASCADE)

class Client(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField()
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    rc = models.CharField(max_length=255)
    ai = models.CharField(max_length=255)
    nif = models.CharField(max_length=255)

class EmplacementArticle(models.Model):
    code = models.CharField(max_length=255)
    description = models.TextField()

class TypeFactures(models.Model):
    code = models.CharField(max_length=255)
    description = models.TextField()


class BonLivraison(models.Model):
    num_liv = models.CharField(max_length=255)
    date_livraison = models.DateTimeField()
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilisez User ici
    annul = models.CharField(max_length=1, default='N')  # Ajout de l'attribut annul avec une valeur par défaut 'N'
    date_annul = models.DateTimeField(null=True, blank=True)  # Ajout de l'attribut date_annul avec null=True et blank=True

def annuler(self):
        self.annul = 'Y'  # Pour marquer la livraison comme annulée
        self.date_annul = timezone.now()  # Pour enregistrer la date d'annulation
        self.save()
def get_details(self):
 return DetailBonLivraison.objects.filter(bon_livraison=self)


class Facture(models.Model):
    num_fac = models.CharField(max_length=255)
    date_facture = models.DateTimeField()
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    type_facture = models.ForeignKey('TypeFactures', on_delete=models.CASCADE)
    num_fac_origine = models.CharField(max_length=255,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilisez User ici
    annul = models.CharField(max_length=1, default='N')  # Ajout de l'attribut annul avec une valeur par défaut 'N'
    date_annul = models.DateTimeField(null=True, blank=True)  # Ajout de l'attribut date_annul avec null=True et blank=True
    totalmontantht = models.DecimalField(max_digits=20, decimal_places=2)
    totalmontantttc = models.DecimalField(max_digits=20, decimal_places=2)


def annuler(self):
        self.annul = 'Y'  # Pour marquer la livraison comme annulée
        self.date_annul = timezone.now()  # Pour enregistrer la date d'annulation
        self.save()
# def get_details(self):
#  return DetailFacture.objects.filter(facture=self)


class DetailBonLivraison(models.Model):
    bon_livraison = models.ForeignKey('BonLivraison', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    quantite_livree = models.IntegerField()

class DetailFacture(models.Model):
    facture = models.ForeignKey('Facture', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    quantite_vendue = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    montantht = models.DecimalField(max_digits=20, decimal_places=2)
    montantttc = models.DecimalField(max_digits=20, decimal_places=2)
    TVA = models.IntegerField()
    remise = models.IntegerField()



