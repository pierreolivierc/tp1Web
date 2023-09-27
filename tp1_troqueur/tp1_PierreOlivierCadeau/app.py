"""
TP1 web 3
"""

import bd
import os
import re
from datetime import date, datetime
from flask import Flask, redirect, render_template, make_response, request, abort
from babel import numbers, dates
from flask_babel import Babel

app = Flask(__name__)

app.config["BABEL_DEFAULT_LOCALE"] = "fr_CA"

babel = Babel(app)

# Liste des sous-répertoires vers "objets"
app.config['MORCEAUX_VERS_AJOUTS'] = ["static", "images", "objets"]

# Pour donner static/images/objets". Assurez-vous que ce dossier existe !
app.config['ROUTE_VERS_AJOUTS'] = "/".join(app.config['MORCEAUX_VERS_AJOUTS'])

app.config['CHEMIN_VERS_AJOUTS'] = os.path.join(
    app.instance_path.replace("instance", ""),
    *app.config['MORCEAUX_VERS_AJOUTS']
)

def lister_routes():
    """Liste les routes pour le menu"""
    return [
        {
            'route': '/',
            'nom': 'Accueil'
        },
        {
            'route': '/ajout_article',
            'nom': "Ajout d'un produit"
        },
        {
            'route': '/liste_tous_les_objets',
            'nom': 'Tous les produits'
        }
    ]



@app.route('/')
def index():
    """Affiche la page d'accueil"""
    objets = recuperation_objet()

    return render_template(
        'accueil.jinja',
        titre_onglet = 'Accueil',
        titre_h2='Les 5 derniers produits à échéanger',
        objets_recuperer = objets,
        src= '../static/images/objets/',
        routes=lister_routes()
    )

def lire_cookie():
    format = request.cookies.get("langue", default="fr_CA")
    return format


@app.route("/ecriture_cookie/<string:langue>")
def ecriture(langue):
    reponse = make_response(redirect('/', code=303))
    reponse.set_cookie('langue', langue)
    return reponse




@app.route('/details', methods=["GET", "POST"])
def details_objet():
    if request.method == "POST":
        id = request.form['objet_choisi']
        objet = recuperation_objet_avec_id(id)
        date_convertie = dates.format_date(objet['date'], locale=lire_cookie())
        return render_template(
            'details_objet.jinja',
            objets_recuperer=objet,
            titre_onglet='Détails',
            date_creation=date_convertie,
            src= '../static/images/objets/',
            modifier='/modifier',
            routes=lister_routes()
        )
    else:
        # Gérez le cas où le formulaire n'a pas été soumis
        # Par exemple, redirigez l'utilisateur vers une autre page
        return redirect('/', code=303)


@app.route('/modifier', methods=["GET", "POST"])
def modifier_objet():
    """Page des détails d'un objet"""
    if request.method == "POST":

        titre = request.form['titre'].strip()
        description = request.form['description'].strip()

        # Supprimez toutes les balises HTML
        titre = re.sub(r'<.*?>', '', titre)
        description = re.sub(r'<.*?>', '', description)

        # récupération du ID catégorie
        categorie_value = request.form['categorie']
        categorie = recuperation_id_categorie(categorie_value)

        maintenant = datetime.now()
        date = maintenant.strftime("%Y-%m-%d")

        id = request.args['objet_choisi']
        objet = recuperation_objet_avec_id(id)

        if not titre or not description:
            return render_template(
                'insertion_reussi_ou_echec.jinja',
                titre_onglet="Ajout d'un produit",
                titre_h2="Ajout d'un produit",
                alerte="alert-danger",
                message="Erreur: le formulaire est incomplet",
                routes=lister_routes()
            ), 400

        nom_image = enregistrement_image()
        if not nom_image :
            return render_template(
                'insertion_reussi_ou_echec.jinja',
                titre_onglet="Ajout d'un produit",
                titre_h2="Ajout d'un produit",
                alerte="alert-danger",
                message="Erreur: l'image est manquante",
                routes=lister_routes()
            ), 400

        supprimer_image(objet["photo"])

        #Modifcation de l'objet dans la base de donnée
        modfication_objet(titre, description, nom_image, categorie, date, id)


        return render_template(
               'insertion_reussi_ou_echec.jinja',
            titre_onglet="Ajout d'une produit",
            titre_h2="Ajout d'une produit",
            alerte="alert-success",
            message= "Le produit a bien été ajouté!",
            routes=lister_routes()
        )
    else:

        id = request.args['objet_choisi']
        objet = recuperation_objet_avec_id(id)

        return render_template(
            'formulaireModification.jinja',
            objets_recuperer=objet,
            titre_h2="Modification d'un produit",
            titre_onglet='Modification du produit',
            routes=lister_routes()
        )

@app.route('/ajout_article', methods=["GET", "POST"])
def ajout_article():
    """Page d'index"""

    if request.method == "POST":
        titre = request.form['titre'].strip()
        description = request.form['description'].strip()

        #Supprimez toutes les balises HTML
        titre = re.sub(r'<.*?>', '', titre)
        description = re.sub(r'<.*?>', '', description)

        #récupération du ID catégorie
        categorie_value = request.form['categorie']
        categorie = recuperation_id_categorie(categorie_value)

        if not titre or not description:
            return render_template(
                'insertion_reussi_ou_echec.jinja',
                titre_onglet="Ajout d'un produit",
                titre_h2="Ajout d'un produit",
                alerte="alert-danger",
                message="Erreur: le formulaire est incomplet",
                routes=lister_routes()
            ), 400


        nom_image = enregistrement_image()
        if not nom_image :
            return render_template(
                'insertion_reussi_ou_echec.jinja',
                titre_onglet="Ajout d'un produit",
                titre_h2="Ajout d'un produit",
                alerte= "alert-danger",
                message="Erreur: l'image est manquante",
                routes=lister_routes()
            ), 400

        maintenant = datetime.now()
        date_creation = maintenant.strftime("%Y-%m-%d")


        # insertion a la bd
        insertion_objet(titre, description, nom_image, categorie, date_creation)


        return render_template(
            'insertion_reussi_ou_echec.jinja',
            titre_onglet="Ajout d'une produit",
            titre_h2="Ajout d'une produit",
            alerte="alert-success",
            message= "Le produit a bien été ajouté!",
            routes=lister_routes()
        )
    else:
        return render_template(
            'formulaire.jinja',
            titre_h2="Ajout d'un produit",
            titre_onglet='Ajout de produit',
            routes=lister_routes()
        )

@app.route('/liste_tous_les_objets')
def liste_article():
    """Faire une boucle pour afficher tous les objets"""

    objets = recuperation_objet()

    #afficher plusieurs card

    return render_template(
        'afficher_tous_les_articles.jinja',
        titre_onglet="Tous les produits",
        titre_h2='Les 5 derniers produits à échéanger',
        objets_recuperer = objets,
        src= '../static/images/objets/',
        routes=lister_routes()
        )


def insertion_objet(u_titre, u_description, u_photo, u_categorie, u_date):
    """insertion d'un objet"""
    try:
        with bd.creer_connexion() as connexion:
            with connexion.get_curseur() as curseur:
                curseur.execute(
                    "INSERT INTO `objets` " +
                    "(`id`, `titre`, `description`, `photo`, `categorie`, `date`) " +
                    "VALUES (NULL, %s, %s, %s, %s , %s)",
                    (u_titre, u_description, u_photo, u_categorie, u_date)
                )
    except Exception as e:
        abort(500, "Une erreur interne du serveur s'est produite")


def modfication_objet(u_titre, u_description, u_photo, u_categorie, u_date, u_id):
    """Modification d'un objet"""
    try:
        with bd.creer_connexion() as connexion:
            with connexion.get_curseur() as curseur:
                curseur.execute(
                    "UPDATE `objets` SET `titre` = %s, `description` = %s, `photo` = %s, `categorie` = %s, `date` = %s " +
                    "WHERE `id` = %s",
                    (u_titre, u_description, u_photo, u_categorie, u_date, u_id)
                )
    except Exception as e:
        abort(500, "Une erreur interne du serveur s'est produite")


def enregistrement_image():
    """Enregistrement de l'image recu au formulaire"""
    fichier = request.files['image']
    if not fichier:
        return None
    # attribution de la date comme nom pour classer les images
    maintenant = datetime.now()
    nom_image = maintenant.strftime("%Y-%m-%d-%Hh%Mm%S") + ".jpg"

    # Mettra des / ou \ dépendamment de l'OS
    chemin_complet = os.path.join(
        app.config['CHEMIN_VERS_AJOUTS'], nom_image
    )

    fichier.save(chemin_complet)

    src = "/" + app.config['ROUTE_VERS_AJOUTS'] + "/" + nom_image

    return nom_image

def supprimer_image(objets):
    # Mettra des / ou \ dépendamment de l'OS
    chemin_complet = os.path.join(
        app.config['CHEMIN_VERS_AJOUTS'], objets
    )

    if os.path.exists(chemin_complet):
        os.remove(chemin_complet)


def recuperation_id_categorie(u_categorie):
    """Pour recuperer un id de catégorie"""
    try:
        with bd.creer_connexion() as connexion:
            with connexion.get_curseur() as curseur:
                # Insertion de objet
                curseur.execute(
                    'SELECT id FROM `categories` '+
                    'WHERE description = %s', (u_categorie,)
                )

                categorie = curseur.fetchone()
                return categorie["id"]
    except Exception as e:
        abort(500, "Une erreur interne du serveur s'est produite")


def recuperation_objet():
    """Pour recuperer tous les objets"""
    try:
        with bd.creer_connexion() as connexion:
            with connexion.get_curseur() as curseur:
                # Sélection de tous les objets
                curseur.execute(
                    'SELECT objets.*, categories.description AS categorie_description ' +
                    'FROM `objets` '+
                    'JOIN `categories` ON objets.categorie = categories.id '+
                    'ORDER BY objets.photo DESC '
                )
                return curseur.fetchall()
    except Exception as e:
        abort(500, "Une erreur interne du serveur s'est produite")


def recuperation_objet_avec_id(u_id):
    """Pour recuperer tous les objets"""
    try:
        with bd.creer_connexion() as connexion:
            with connexion.get_curseur() as curseur:
                # Sélection de tous les objets
                curseur.execute(
                    'SELECT objets.*, categories.description AS categorie_description '+
                    'FROM `objets` '+
                    'JOIN `categories` ON objets.categorie = categories.id '+
                    'WHERE objets.id =  %s', (u_id, )
                )
                return curseur.fetchone()
    except Exception as e:
        abort(500, "Une erreur interne du serveur s'est produite")