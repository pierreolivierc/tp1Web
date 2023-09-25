"""
TP1 web 3
"""
import re
import bd
import os
import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

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
    return render_template(
        'article.jinja',
        titre_onglet = 'Accueil',
        titre_h2='Les 5 derniers produits à échéanger',
        titre_h3='Test',
        src_image_article= '../static/images/image_par_default.jpg',
        message="Description d'article!",
        details= '/details',
        routes=lister_routes()
    )

@app.route('/details')
def details_objet():
    """Page des détails d'un objet"""
    return render_template(
        'details_objet.jinja',
        titre_onglet='Accueil',
        titre_h3='titre detail',
        titre_h4='Test',
        src_image_article='../static/images/image_par_default.jpg',
        message="Description d'article!",
        modifier='/modifier',
        routes=lister_routes()
    )

@app.route('/modifier', methods=["GET", "POST"])
def modifier_objet():
    """Page des détails d'un objet"""
    if request.method == "POST":
        titre = request.form['titre']
        description = request.form['description']

        # récupération du ID catégorie
        categorie_value = request.form['categorie']
        categorie = recuperation_id_categorie(categorie_value)

        # attribution de la date comme nom pour classer les images
        maintenant = datetime.datetime.now()
        nom_image = maintenant.strftime("%Y-%m-%d-%Hh%Mm%S") + ".jpg"

        # insertion a la bd
        insertion_objet(titre, description, nom_image, 1)

        fichier = request.files['image']

        # Mettra des / ou \ dépendamment de l'OS
        chemin_complet = os.path.join(
            app.config['CHEMIN_VERS_AJOUTS'], nom_image
        )

        fichier.save(chemin_complet)

        src = "/" + app.config['ROUTE_VERS_AJOUTS'] + "/" + nom_image

        return render_template(
            'article.jinja',
            titre_onglet='Modification du produit',
            titre_h2="Modification du produit",
            titre_h3=titre,
            sous_titre=categorie,
            # trouvé une facon d'enregistrer l'image et l'afficher
            src_image_article='../static/images/image_par_default.jpg',
            message=description,
            routes=lister_routes()
        )
    else:
        return render_template(
            'formulaire.jinja',
            titre_h2="Modification du produit",
            titre_onglet="Modification du produit",
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

        # attribution de la date comme nom pour classer les images
        maintenant = datetime.datetime.now()
        nom_image = maintenant.strftime("%Y-%m-%d-%Hh%Mm%S") + ".jpg"

        # insertion a la bd
        insertion_objet(titre, description, nom_image, 1)

        fichier = request.files['image']

        # Mettra des / ou \ dépendamment de l'OS
        chemin_complet = os.path.join(
        app.config['CHEMIN_VERS_AJOUTS'], nom_image
        )

        fichier.save(chemin_complet)

        src = "/" + app.config['ROUTE_VERS_AJOUTS'] + "/" + nom_image


        return render_template(
            'article.jinja',
            titre_onglet='Ajout de produit',
            titre_h2="Ajout d'un produit",
            titre_h3= titre,
            sous_titre= categorie,
            # trouvé une facon d'enregistrer l'image et l'afficher
            src_image_article= '../static/images/image_par_default.jpg',
            message= description,
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

    tous_les_objets = recuperation_objet()

    #afficher plusieurs card
    for un_objet in tous_les_objets:
        return render_template(
            'article.jinja',
            titre_onglet='Tous les produits',
            titre_h1='Bonjour!',
            message= tous_les_objets,
            routes=lister_routes()
        )


def insertion_objet(u_titre, u_description, u_photo, u_categorie):
    """insertion d'un objet"""

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            # Insertion de objet
            curseur.execute(
                "INSERT INTO `objets` " +
                "(`id`, `titre`, `description`, `photo`, `categorie`) " +
                "VALUES (NULL, %s, %s, %s, %s)",
                (u_titre, u_description, u_photo, u_categorie)
            )



def recuperation_id_categorie(u_categorie):
    """Pour recuperer un id de catégorie"""

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            # Insertion de objet
            curseur.execute(
                'SELECT id FROM `categories` '+
                'WHERE description = %s', (u_categorie,)
            )
            return curseur.fetchone()

def recuperation_objet():
    """Pour recuperer tous les objets"""

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            # Insertion de objet
            curseur.execute(
                'SELECT * FROM `objets` '
            )
            return curseur.fetchone()