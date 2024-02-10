from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', login_required(views.index), name="index"),    path('form/', views.form,name="form"),
    # url client
    path('client/',login_required(views.indexclient),name="indexclient"),
    path('addclient/', views.addclient,name="addclient"),
    path('deleteclient/<int:id>', views.deleteclient,name="deleteclient"),
    path('updateclient/<int:id>', views.updateclient,name="updateclient"),
    # url article
    path('article/', login_required(views.indexarticle),name="indexarticle"),
    path('addarticle/', views.addarticle,name="addarticle"),
    path('deletearticle/<int:id>', views.deletearticle,name="deletearticle"),
    path('updatearticle/<int:id>', views.updatearticle,name="updatearticle"),
    #  url emplacement article
    path('emplacement/', login_required(views.indexemplacement),name="indexemplacement"),
    path('addemplacement/', views.addemplacement,name="addemplacement"),
    path('deleteemplacement/<int:id>', views.deleteemplacement,name="deleteemplacement"),
    path('updateemplacement/<int:id>', views.updateemplacement,name="updateemplacement"),
    # utilisateur
    path('utilisateur/', login_required(views.indexutilisateur),name="indexutilisateur"),
    path('addutilisateur/', views.addutilisateur, name='addutilisateur'),
    path('updateutilisateur/<int:id>', views.updateutilisateur, name='updateutilisateur'),
    path('deleteutilisateur/<int:id>/', views.deleteutilisateur, name='deleteutilisateur'),
    # livraison
    path('livraison/', login_required(views.indexlivraison),name="indexlivraison"),
    path('addlivraison/', views.addlivraison,name="addlivraison"),
    path('get_details/<int:bon_livraison_id>/', views.get_details, name='get_details'),
    path('updatelivraison/<int:bon_livraison_id>/', views.updatelivraison, name='updatelivraison'),
    path('annulerlivraison/<int:bon_livraison_id>/', views.annulerlivraison, name='annulerlivraison'),
    path('generate_pdf/<int:bon_livraison_id>', views.generate_pdf, name='generate_pdf'),
    # facturation
    path('facturation/', login_required(views.indexfacturation),name="indexfacturation"),
    path('addfacturation/', views.addfacturation,name="addfacturation"),
    path('get_details_facture_original/<int:facture_id>/', views.get_details_facture_original, name='get_details_facture_original'),
    path('get_details_facture/<int:facture_id>/', views.get_details_facture, name='get_details_facture'),
    path('annulerfacture/<int:facture_id>/', views.annulerfacture, name='annulerfacture'),
    path('generate_pdf_facture/<int:facture_id>', views.generate_pdf_facture, name='generate_pdf_facture'),









    # path('update/uprec/<int:id>', views.uprec,name="uprec"),
    # path('testhome/', views.testhome,name="testhome"),
   

]