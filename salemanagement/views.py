from datetime import datetime
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from .models import Client,Article,EmplacementArticle,BonLivraison,DetailBonLivraison,Facture,DetailFacture,TypeFactures
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Assurez-vous d'importer le modèle User
from django.contrib.auth.hashers import make_password
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import Spacer
from pprint import pprint
from django.db import transaction
import pdb







@login_required
def index(request):
    user = request.user
    return render(request,'index.html', {'user': user})

def form(request):
    return render(request,'form.html')

# fichier client 

def indexclient(request):
    client=Client.objects.all()
    return render(request,'referentiel/client.html',{'client':client})

def addclient(request):
    nomclient=request.POST['nom']
    prenomclient=request.POST['prenom']
    adresseclient=request.POST['adresse']
    emailclient=request.POST['email']
    telephoneclient=request.POST['telephone']
    rcclient=request.POST['rc']
    aiclient=request.POST['ai']
    nifclient=request.POST['nif']
    client=Client(nom=nomclient,prenom=prenomclient,adresse=adresseclient,email=emailclient,telephone=telephoneclient,rc=rcclient,ai=aiclient,nif=nifclient)
    client.save()
    return redirect('/client')

def updateclient(request,id):
    nomclient=request.POST['nom']
    prenomclient=request.POST['prenom']
    adresseclient=request.POST['adresse']
    emailclient=request.POST['email']
    telephoneclient=request.POST['telephone']
    rcclient=request.POST['rc']
    aiclient=request.POST['ai']
    nifclient=request.POST['nif']
    client=Client.objects.get(id=id)
    client.nom=nomclient
    client.prenom=prenomclient
    client.adresse=adresseclient
    client.email=emailclient
    client.telephone=telephoneclient
    client.rc=rcclient
    client.ai=aiclient
    client.nif=nifclient
    client.save()
    return redirect('/client')

def deleteclient(request,id):
    client=Client.objects.get(id=id)
    client.delete()
    return redirect("/client")

# fichier article

def indexarticle(request):
    article=Article.objects.all()
    emplacement=EmplacementArticle.objects.all()
    return render(request,'referentiel/article.html',{'article':article,'emplacement':emplacement})

def addarticle(request):
    codearticle = request.POST['code']
    descriptionarticle = request.POST['description']
    prix_uarticle = request.POST['prix_unitaire']
    stockarticle = request.POST['stock']
    emplacementarticle_id = request.POST['emplacement_id']  # Utilisez 'emplacement_id' pour obtenir l'ID de l'emplacement

    
    emplacement_instance = EmplacementArticle.objects.get(pk=emplacementarticle_id)
    article = Article(code=codearticle,description=descriptionarticle,prix_unitaire=prix_uarticle,stock=stockarticle,emplacement=emplacement_instance) # Assurez-vous d'assigner l'instance d'emplacement correctement
    article.save()
    return redirect('/article')
   

def updatearticle(request,id):
    codearticle=request.POST['code']
    descriptionarticle=request.POST['description']
    prix_uarticle=request.POST['prix_unitaire']
    stockarticle=request.POST['stock']
    emplacementarticle=request.POST['emplacement_id']
    article=Article.objects.get(id=id)
    emplacement_instance = EmplacementArticle.objects.get(pk=emplacementarticle)
    article.code=codearticle
    article.description=descriptionarticle
    article.prix_unitaire=prix_uarticle
    article.stock=stockarticle
    article.emplacement=emplacement_instance
    article.save()
    return redirect('/article')

def deletearticle(request,id):
    article=Article.objects.get(id=id)
    article.delete()
    return redirect("/article")

# fichier emplacement

def indexemplacement(request):
    emplacement=EmplacementArticle.objects.all()
    return render(request,'referentiel/emplacement.html',{'emplacement':emplacement})

def addemplacement(request):
    codeemplacement=request.POST['code']
    descriptionemplacement=request.POST['description']
    emplacement=EmplacementArticle(code=codeemplacement,description=descriptionemplacement)
    emplacement.save()
    return redirect('/emplacement')

def updateemplacement(request,id):
    codeemplacement=request.POST['code']
    descriptionemplacement=request.POST['description']
    emplacement=EmplacementArticle.objects.get(id=id)
    emplacement.code=codeemplacement
    emplacement.description=descriptionemplacement
    emplacement.save()
    return redirect('/emplacement')

def deleteemplacement(request,id):
    emplacement=EmplacementArticle.objects.get(id=id)
    emplacement.delete()
    return redirect("/emplacement")

# fichier utilisateur

def indexutilisateur(request):
    utilisateur=User.objects.all()
    return render(request,'referentiel/utilisateur.html',{'utilisateur':utilisateur})

def addutilisateur(request):
    firstname = request.POST['first_name']
    lastname = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password1']
    hashed_password = make_password(password)
    utilisateur = User(
        first_name=firstname,
        last_name=lastname,
        username=username,
        email=email,
        password=hashed_password,
        last_login=datetime.now()  # Assurez-vous d'assigner l'instance d'emplacement correctement
    )
    utilisateur.save()
    return redirect('/utilisateur')


def updateutilisateur(request,id):
    firstname = request.POST['first_name']
    lastname = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password1']
    hashed_password = make_password(password)
    utilisateur=User.objects.get(id=id)
    utilisateur.first_name=firstname
    utilisateur.last_name=lastname
    utilisateur.username=username
    utilisateur.email=email
    utilisateur.password=hashed_password
    utilisateur.save()
    return redirect('/utilisateur')
   

def deleteutilisateur(request, id):
    # Assurez-vous que l'utilisateur existe avant de le supprimer
    try:
        user = User.objects.get(id=id)
        user.delete()
        # Redirigez l'utilisateur vers une page appropriée après la suppression
        return redirect('/utilisateur')
    except User.DoesNotExist:
        # Gérer le cas où l'utilisateur n'existe pas
        return HttpResponse("L'utilisateur n'existe pas.")

# traiement livraison
def indexlivraison(request):
    # Récupérez les données de la table BonLivraison et DetailBonLivraison
    bon_livraisons = BonLivraison.objects.filter(annul='N')
    clients=Client.objects.all()
    articles=Article.objects.all()
    detail_bon_livraisons = DetailBonLivraison.objects.all()

    detail_bon_livraisons_json = serializers.serialize('json', detail_bon_livraisons)

    # Ajoutez les données récupérées au dictionnaire contextuel
    context = {
        'bon_livraisons': bon_livraisons,
        'detail_bon_livraisons_json': detail_bon_livraisons_json,
        'clients' : clients,
        'articles' : articles,
        'value': datetime.now()
    }

    return render(request, 'livraison/bonlivraison.html', context)

def addlivraison(request):
    try:
        current_datetime = datetime.now()
        current_year = current_datetime.year
        last_livraison = BonLivraison.objects.filter(num_liv__startswith=f'LIV{current_year}').order_by('-num_liv').first()

        if last_livraison:
            last_code = last_livraison.num_liv
            last_sequence = int(last_code[-5:])
            next_sequence = last_sequence + 1
        else:
            next_sequence = 1

        user_id = request.user.id
        num_liv = f'LIV{current_year}{next_sequence:05d}'
        client_id = request.POST['client_id']
        client = Client.objects.get(pk=client_id)
        user = User.objects.get(pk=user_id)
        livraison = BonLivraison(num_liv=num_liv,date_livraison=current_datetime,client=client,user=user)
        livraison.save()

        article_ids = request.POST.getlist('article_id')
        qtes = request.POST.getlist('qte')

        if len(article_ids) == len(qtes):
            for i in range(len(article_ids)):
                article_id = article_ids[i]
                article = Article.objects.get(pk=article_id)
                qte_livree = qtes[i]
                detail_livraison = DetailBonLivraison(
                    article=article,
                    quantite_livree=qte_livree,
                    bon_livraison=livraison
                )
                detail_livraison.save()
        else:
            # Gérez l'erreur ici, par exemple, en renvoyant un message d'erreur ou en enregistrant des journaux
            print("Les listes article_id et qte n'ont pas la même longueur.")


        return redirect('/livraison')
    except Exception as e:
        # Gérez les erreurs ici (par exemple, affichez-les dans la console)
        print(f"Erreur lors de l'enregistrement de la livraison : {e}")
        return redirect('/livraison')

def get_details(request, bon_livraison_id):
    # Récupérez les détails de la livraison en fonction de bon_livraison_id
    details = DetailBonLivraison.objects.filter(bon_livraison_id=bon_livraison_id)

    # Créez une liste de dictionnaires contenant les détails
    details_data = []

    for detail in details:
        details_data.append({
            'article_id': detail.article.id,  # Supposons que vous avez une relation entre DetailBonLivraison et Article
            'code_article': detail.article.code,
            'description': detail.article.description,
            'prix_unitaire': detail.article.prix_unitaire,
            'quantite_livree': detail.quantite_livree,
            'bon_livraison_id': detail.bon_livraison_id,
            # Ajoutez d'autres champs de détail ici
        })

    # Renvoyez les détails au format JSON
    return JsonResponse({'details': details_data})


def updatelivraison(request, bon_livraison_id):
    client_id=request.POST['client_id']
    date_livraison=request.POST['date_livraison']
    format_string = '%Y-%m-%dT%H:%M'
    formatted_date = datetime.strptime(date_livraison, format_string)
    livraison=BonLivraison.objects.get(id=bon_livraison_id)
    client_instance = Client.objects.get(pk=client_id)
    livraison.client=client_instance
    livraison.date_livraison=formatted_date
    livraison.save()

    article_ids = request.POST.getlist('article_id')
    qtes = request.POST.getlist('qte')

    if len(article_ids) == len(qtes):
            # Supprimez tous les détails de la livraison existants pour les recréer
            DetailBonLivraison.objects.filter(bon_livraison=livraison).delete()

            for i in range(len(article_ids)):
                article_id = article_ids[i]
                article = Article.objects.get(pk=article_id)
                qte_livree = qtes[i]
                detail_livraison = DetailBonLivraison(
                    article=article,
                    quantite_livree=qte_livree,
                    bon_livraison=livraison
                )
                detail_livraison.save()
    return redirect('/livraison')
   
def annulerlivraison(request,bon_livraison_id):
    livraison=BonLivraison.objects.get(id=bon_livraison_id)
    livraison.annul='O'
    livraison.date_annul=datetime.now()
    livraison.save()

    return redirect('/livraison')




def generate_pdf(request, bon_livraison_id):
    livraison = BonLivraison.objects.get(id=bon_livraison_id)
    detaillivraisons = DetailBonLivraison.objects.filter(bon_livraison=bon_livraison_id)

    # Créez un objet BytesIO pour stocker le PDF généré
    pdf_buffer = BytesIO()

    # Créez un objet SimpleDocTemplate pour le PDF
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)

    # Créez une liste de données pour le tableau
    table_data = [['Code article', 'Description', 'Quantité livrée', 'Prix unitaire']]

    # Remplissez la liste de données avec les détails de livraison
    for detaillivraison in detaillivraisons:
        code_article = detaillivraison.article.code
        description = detaillivraison.article.description
        quantite_livree = detaillivraison.quantite_livree
        prix_unitaire = detaillivraison.article.prix_unitaire
        table_data.append([code_article, description, quantite_livree, prix_unitaire])

    # Créez un objet Table avec les données et la taille des colonnes
    table = Table(table_data, colWidths=[80, 180, 80, 80])

    # Appliquez un style au tableau
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table.setStyle(style)

    styles = getSampleStyleSheet()
    num_liv_paragraph = Paragraph(f"<b>Bon livraison N°:</b> {livraison.num_liv}", styles['Title'])
    date_impression_paragraph = Paragraph(f"<b>Date d'impression:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal'])
    
    # Ajoutez de l'espace entre la date d'impression et la date de livraison
    spacer = Spacer(1, 10)

    # Créez un paragraphe pour la date de livraison et le client dans la même ligne
    date_livraison_client_paragraph = Paragraph(f"<b>Date livraison:</b> {livraison.date_livraison}              &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; <b>Client:</b> {livraison.client.nom} {livraison.client.prenom}", styles['Normal'])

    # Créez un objet Spacer pour ajuster l'espace entre les éléments
    spacer = Spacer(1, 20)

    # Ajoutez le tableau et les Paragraphs au PDF
    story = [num_liv_paragraph, date_impression_paragraph, spacer, date_livraison_client_paragraph, spacer, table]
    # Terminez le dessin du PDF
    doc.build(story)

    # Réglez le curseur de l'objet BytesIO au début du flux
    pdf_buffer.seek(0)

    # Retournez le PDF en réponse HTTP
    response = FileResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{livraison.num_liv}_livraison.pdf"'
    return response

# traitement facturation
def indexfacturation(request):
    
    facture_proforma = Facture.objects.filter(annul='N', type_facture_id=1).order_by('-id')
    facture_normale = Facture.objects.filter(annul='N',type_facture_id=2).order_by('-id')
    facture_avoir = Facture.objects.filter(annul='N',type_facture_id=3).order_by('-id')

    clients=Client.objects.all()
    articles=Article.objects.all()
    detail_facture = DetailFacture.objects.all()

    detail_facture_json = serializers.serialize('json', detail_facture)

    # Ajoutez les données récupérées au dictionnaire contextuel
    context = {
        'facture_proforma': facture_proforma,
        'facture_normale': facture_normale,
        'facture_avoir': facture_avoir,
        'detail_facture_json': detail_facture_json,
        'clients' : clients,
        'articles' : articles,
        'value': datetime.now()
    }

    return render(request, 'facturation/facturation.html', context)

def addfacturation(request):
  
    try:
        current_datetime = datetime.now()
        # date_str = request.POST['date_facture']
        # current_datetime1 =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_year = current_datetime.year
        type_facture_id=request.POST['type_facture_id']
        type_facture_instance = TypeFactures.objects.get(pk=type_facture_id)
        num_facture_origine = request.POST['num_fac_origine']

        
        # pprint(vars(type_facture_instance))

        # Ajoutez une condition pour déterminer le préfixe en fonction de type_facture_id
        if type_facture_instance.id == 1:
            prefix = 'PRO'
        elif type_facture_instance.id == 2:
            prefix = 'FAC'
        elif type_facture_instance.id == 3:
            prefix = 'AV'
            facture_origine = Facture.objects.get(num_fac=num_facture_origine)

            # Mettre à jour la facture d'origine
            facture_origine.annul = 'Y'  # Mettez la valeur correcte selon votre modèle
            facture_origine.date_annul = datetime.now()
            facture_origine.save()
        else:
            # Gérer d'autres valeurs si nécessaire
            prefix = 'OTHER'

        last_facture = Facture.objects.filter(num_fac__startswith=f'{prefix}{current_year}').order_by('-num_fac').first()

        if last_facture:
            last_code = last_facture.num_fac
            last_sequence = int(last_code[-5:])
            next_sequence = last_sequence + 1
        else:
            next_sequence = 1

        num_fac = f'{prefix}{current_year}{next_sequence:05d}'
        user_id = request.user.id
        client_id = request.POST['client_id']
        totalmontantht = request.POST['totalmontantht']
        totalmontantttc = request.POST['totalmontantttc']

        pprint(num_facture_origine)
        client = Client.objects.get(pk=client_id)
       
        user = User.objects.get(pk=user_id)
        facture = Facture(num_fac=num_fac,date_facture=current_datetime,client=client,type_facture=type_facture_instance,num_fac_origine=num_facture_origine,user=user,totalmontantht=totalmontantht,totalmontantttc=totalmontantttc)
        facture.save()


        article_ids = request.POST.getlist('article_id')
        qtes = request.POST.getlist('qte')
        prix_u = request.POST.getlist('prix_u')
        tva = request.POST.getlist('TVA')
        remise = request.POST.getlist('remise')
        montant_ht = request.POST.getlist('montantht')
        montant_ttc = request.POST.getlist('montantttc')

        if len(article_ids) == len(qtes):
            for i in range(len(article_ids)):
                article_id = article_ids[i]
                article = Article.objects.get(pk=article_id)
                qte_vendu = qtes[i]
                prix_unitaire = prix_u[i]
                tauxtva = tva[i]
                tauxremise = remise[i]
                montantht = montant_ht[i]
                montantttc = montant_ttc[i]

                detail_facture = DetailFacture(
                    article=article,
                    quantite_vendue=qte_vendu,
                    prix_unitaire=prix_unitaire,
                    TVA=tauxtva,
                    remise=tauxremise,
                    montantht=montantht,
                    montantttc=montantttc,
                    facture=facture
                )
                detail_facture.save()

            # Mise à jour de la quantité en fonction du type de facture
            for i in range(len(article_ids)):
                article_id = article_ids[i]
                article = Article.objects.get(pk=article_id)
                qte_vendu_str = qtes[i]
                print(type_facture_instance.id)
                # Convertir qte_vendu_str en un entier
                qte_vendu = int(qte_vendu_str)
                # Mise à jour de la quantité en fonction du type de facture
                if type_facture_instance.id == 2:
                    article.stock -= qte_vendu  # Soustraction pour les factures de type 1
                elif type_facture_instance.id == 3:
                    article.stock += qte_vendu  # Addition pour les factures de type 2
                article.save()
        else:
            # Gérez l'erreur ici, par exemple, en renvoyant un message d'erreur ou en enregistrant des journaux
            print("Les listes article_id et qte n'ont pas la même longueur.")

        return redirect('/facturation')
    except Exception as e:
        # Gérez les erreurs ici (par exemple, affichez-les dans la console)
        print(f"Erreur lors de l'enregistrement de la livraison : {e}")
        return redirect('/facturation')

def get_details_facture_original(request, facture_id):
    # Récupérez les détails de la livraison en fonction de bon_livraison_id
    details = DetailFacture.objects.filter(facture_id=facture_id)

    print(details)

    # Créez une liste de dictionnaires contenant les détails
    details_data = []

    for detail in details:
        details_data.append({
            'article_id': detail.article.id,  # Supposons que vous avez une relation entre DetailBonLivraison et Article
            'code_article': detail.article.code,
            'description': detail.article.description,
            'prix_unitaire': detail.article.prix_unitaire,
            'quantite_vendue': detail.quantite_vendue,
            'montantht': detail.montantht,
            'montantttc': detail.montantttc,
            'TVA': detail.TVA,
            'remise': detail.remise,
            'facture_id': detail.facture_id,
            # Ajoutez d'autres champs de détail ici
        })

    # Renvoyez les détails au format JSON
    return JsonResponse({'details': details_data})

def get_details_facture(request, facture_id):
    # Récupérez les détails de la livraison en fonction de bon_livraison_id
    details = DetailFacture.objects.filter(facture_id=facture_id)

    print(details)

    # Créez une liste de dictionnaires contenant les détails
    details_data = []

    for detail in details:
        details_data.append({
            'article_id': detail.article.id,  # Supposons que vous avez une relation entre DetailBonLivraison et Article
            'code_article': detail.article.code,
            'description': detail.article.description,
            'prix_unitaire': detail.article.prix_unitaire,
            'quantite_vendue': detail.quantite_vendue,
            'montantht': detail.montantht,
            'montantttc': detail.montantttc,
            'TVA': detail.TVA,
            'remise': detail.remise,
            'facture_id': detail.facture_id,
            # Ajoutez d'autres champs de détail ici
        })

    # Renvoyez les détails au format JSON
    return JsonResponse({'details': details_data})

def annulerfacture(request,facture_id):
    facture=Facture.objects.get(id=facture_id)
    facture.annul='O'
    facture.date_annul=datetime.now()
    facture.save()

    return redirect('/facturation')

def generate_pdf_facture(request, facture_id):
    # Récupérez la facture et ses détails
    facture = get_object_or_404(Facture, pk=facture_id)
    details = DetailFacture.objects.filter(facture=facture)

    # Créez un objet BytesIO pour stocker le PDF
    buffer = BytesIO()

    # Créez le PDF avec ReportLab
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Liste pour contenir le contenu du PDF (Story)
    story = []

    # Ajoutez le titre "Facture" avec le numéro de facture, le nom du client et les dates
    title_content = f"Facture {facture.num_fac} <br/>"

    # Définissez le style du titre
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=getSampleStyleSheet()['Heading1'],
        alignment=1  # 0=left, 1=center, 2=right
    )
    title = Paragraph(title_content, title_style)

    
    date_facture = f"Date de Facture: {facture.date_facture.strftime('%Y-%m-%d')} "
    date_impression = f"Date d'Impression: {datetime.now().strftime('%Y-%m-%d')}<br/><br/><br/><br/><br/><br/>"

    client_content = f"Client: {facture.client.nom}<br/><br/>"


    date_style = getSampleStyleSheet()['BodyText']

    date_f= Paragraph(date_facture, date_style)
    date_style_right_aligned = ParagraphStyle(
    'RightAligned',  # Nom du style
    parent=date_style,  # Utilisez le style existant comme parent
    alignment=2,  # 2 signifie alignement à droite, 0 est à gauche, 1 est centré
)

# Utilisez le nouveau style pour la date d'impression
    date_im = Paragraph(date_impression, date_style_right_aligned)
   

    client_style = getSampleStyleSheet()['BodyText']
    client = Paragraph(client_content, client_style)

    # Ajoutez les éléments au contenu (Story)
    story.extend([title,  date_im, date_f,client])

    # Ajoutez une ligne vide pour l'espace
    story.append(Spacer(1, 12))

    # Construisez le tableau des détails de la facture
    table_data = [['Code Article', 'Désignation', 'Quantité', 'Prix Unitaire', 'Remise', 'TVA', 'Montant HT', 'Montant TTC']]

    # Remplissez le tableau avec les détails de la facture
    for detail in details:
        table_data.append([
            detail.article.code,
            detail.article.description,
            detail.quantite_vendue,
            detail.prix_unitaire,
            detail.remise,
            detail.TVA,
            detail.montantht,
            detail.montantttc,
        ])

    # Ajoutez la ligne de totaux
    total_montant_ht = sum(detail.montantht for detail in details)
    total_montant_ttc = sum(detail.montantttc for detail in details)

    table_data.append(['Total Montant', '', '', '', '', ' ', total_montant_ht, total_montant_ttc])

    table = Table(table_data)

    # Définissez le style de la table
    style = TableStyle([
        ('INNERGRID', (5, 0), (5, -1), 0.25, colors.white),  # Supprimez la bordure intérieure à droite de la colonne 5
        ('BOTTOMPADDING', (0, -1), (-1, -1), 0),  # Supprimez le padding inférieur pour la dernière ligne
    ])

    # Appliquez le style à la table
    table.setStyle(style)
    story.append(table)

    # Construisez le PDF avec le contenu (Story)
    pdf.build(story)

    # Déplacez le tampon au début du flux pour la lecture
    buffer.seek(0)

    # Créez une réponse HTTP avec le contenu du PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{facture.num_fac}_facture.pdf"'
    response.write(buffer.getvalue())

    return response