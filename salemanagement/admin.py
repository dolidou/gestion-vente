from django.contrib import admin
from .models import Client,BonLivraison,DetailBonLivraison,Facture

class ClientAdmin(admin.ModelAdmin):
    list_display="nom","prenom","email","adresse","telephone","rc","ai","nif"

admin.site.register(Client,ClientAdmin)

class BonLivraisonAdmin(admin.ModelAdmin):
    list_display="num_liv","date_livraison","client_id","user_id"

admin.site.register(BonLivraison,BonLivraisonAdmin)

class DetailBonLivraisonAdmin(admin.ModelAdmin):
    list_display="quantite_livree","article_id","bon_livraison"

admin.site.register(DetailBonLivraison,DetailBonLivraisonAdmin)

class FactureAdmin(admin.ModelAdmin):
    list_display="num_fac","date_facture","totalmontantht","totalmontantttc","client_id","user_id","type_facture_id","num_fac_origine"

admin.site.register(Facture,FactureAdmin)

# Register your models here.
