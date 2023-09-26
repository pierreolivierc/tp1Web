"""
TP1 web 3
"""
import re
import bd
import os
import datetime
from flask import Flask, redirect, render_template, request

app = Flask(__name__)
# TODO AJOUTER COLONE DATE DANS MY SQL

# Liste des sous-répertoires vers "ajouts"
app.config['MORCEAUX_VERS_AJOUTS'] = ["static", "images", "ajouts"]

# Pour donner static/images/ajouts". Assurez-vous que ce dossier existe !
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
        src= '../static/images/ajouts/',
        routes=lister_routes()
    )


@app.route('/details', methods=["GET", "POST"])
def details_objet():
    if request.method == "POST":
        id = request.form['objet_choisi']
        objet = recuperation_objet_avec_id(id)

        return render_template(
            'details_objet.jinja',
            objets_recuperer=objet,
            titre_onglet='Accueil',
            src= '../static/images/ajouts/',
            modifier='/modifier',
            routes=lister_routes()
        )
    else:
        # Gérez le cas où le formulaire n'a pas été soumis
        # Par exemple, redirigez l'utilisateur vers une autre page
        return redirect('/')


@app.route('/modifier', methods=["GET", "POST"])
def modifier_objet():
    """Page des détails d'un objet"""
    if request.method == "POST":
        id = request.form['objet_choisi']

        titre = request.form['titre']
        description = request.form['description']

        # récupération du ID catégorie
        categorie_value = request.form['categorie']
        categorie = recuperation_id_categorie(categorie_value)

        nom_image = enregistrement_image()

        date = request.form['date_input']


        return render_template(
            'insertion_reussi_ou_echec.jinja',
            titre_onglet='Modification du produit',
            titre_h2="Insertion de l'image",
            message="L'insertion de l'image à bien réussi!",
            routes=lister_routes()
        )
    else:
        return render_template(
            'formulaire.jinja',
            titre_h2="Modification d'un produit",
            titre_onglet='Modification du produit',
            routes=lister_routes()
        )

@app.route('/ajout_article', methods=["GET", "POST"])
def ajout_article():
    """Page d'index"""

    if request.method == "POST":
        titre = request.form['titre']
        description = request.form['description']

        #récupération du ID catégorie
        categorie_value = request.form['categorie']
        categorie = recuperation_id_categorie(categorie_value)

        nom_image = enregistrement_image()

        date = request.form['date_input']

        # insertion a la bd
        insertion_objet(titre, description, nom_image, categorie, date)


        return render_template(
            'insertion_reussi_ou_echec.jinja',
            titre_onglet='Ajout de produit',
            titre_h2="Insertion de l'image",
            message= "L'insertion de l'image à bien réussi!",
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
    """faire une boucle pour afficher tous les objets"""

    objets = recuperation_objet()

    #afficher plusieurs card

    return render_template(
        'afficher_tous_les_articles.jinja',
        titre_onglet='Accueil',
        titre_h2='Les 5 derniers produits à échéanger',
        objets_recuperer = objets,
        src= '../static/images/ajouts/',
        details='/details',
        routes=lister_routes()
        )


def insertion_objet(u_titre, u_description, u_photo, u_categorie, u_date):
    """insertion d'un objet"""

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute(
                "INSERT INTO `objets` " +
                "(`id`, `titre`, `description`, `photo`, `categorie`, `date`) " +
                "VALUES (NULL, %s, %s, %s, %s , %s)",
                (u_titre, u_description, u_photo, u_categorie, u_date)
            )

def modfication_objet(u_titre, u_description, u_photo, u_categorie, u_date, u_id):
    """Modification d'un objet"""

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute(
                "UPDATE `objets` SET `titre` = %s, `description` = %s, `photo` = %s, `categorie` = %s, `date` = %s " +
                "WHERE `id` = %s",
                (u_titre, u_description, u_photo, u_categorie, u_date, u_id)
            )

def enregistrement_image():
    """Enregistrement de l'image recu au formulaire"""
    fichier = request.files['image']
    if not fichier:
        # L'utilisateur n'a pas envoyé de fichier
        # ne fonctionne pas pour le moment
        fichier = '../static/images/image_par_default.jpg'

    # attribution de la date comme nom pour classer les images
    maintenant = datetime.datetime.now()
    nom_image = maintenant.strftime("%Y-%m-%d-%Hh%Mm%S") + ".jpg"

    # Mettra des / ou \ dépendamment de l'OS
    chemin_complet = os.path.join(
        app.config['CHEMIN_VERS_AJOUTS'], nom_image
    )

    fichier.save(chemin_complet)

    src = "/" + app.config['ROUTE_VERS_AJOUTS'] + "/" + nom_image

    return nom_image

def recuperation_id_categorie(u_categorie):
    """Pour recuperer un id de catégorie"""

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            # Insertion de objet
            curseur.execute(
                'SELECT id FROM `categories` '+
                'WHERE description = %s', (u_categorie,)
            )

            categorie = curseur.fetchone()
            return categorie["id"]

def recuperation_objet():
    """Pour recuperer tous les objets"""

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


def recuperation_objet_avec_id(u_id):
    """Pour recuperer tous les objets"""

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            # Sélection de tous les objets
            curseur.execute(
                'SELECT objets.*, categories.description AS categorie_description '+
                'FROM `objets` '+
                'JOIN `categories` ON objets.categorie = categories.id '+
                'WHERE objets.id =  %s', (u_id,)
            )
            return curseur.fetchone()