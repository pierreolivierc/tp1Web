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
            'route': '/details_objet',
            'nom': 'Tous les produits'
        }
    ]



@app.route('/')
def index():
    """Affiche la page d'accueil"""
    return render_template(
        'article.jinja',
        titre_h2='Les 5 derniers produits à échéanger',
        titre_h3='Test',
        src_image_article= '../static/images/image_par_default.jpg',
        message="Description d'article!",
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
        #categorie = recuperation_id_categorie(categorie_value)

        # attribution de la date comme nom pour classer les images
        maintenant = datetime.datetime.now()
        nom_image = maintenant.strftime("%Y-%m-%d-%H:%M:%S") + ".jpg"

        # insertion a la bd
        insertion_objet(titre, description, nom_image, 1)

        # fichier = request.files['image']

        # if not fichier:
            # ajout d'une image par défault
            # src = '../static/images/image_par_default.jpg'
        # else:
            # Mettra des / ou \ dépendamment de l'OS
            # chemin_complet = os.path.join(
            #    app.config['CHEMIN_VERS_AJOUTS'], nom_image
            # )

            # fichier.save(chemin_complet)

            # src = "/" + app.config['ROUTE_VERS_AJOUTS'] + "/" + nom_image


        return render_template(
            'article.jinja',
            titre_h2='Les 5 derniers produits à échéanger',
            titre_h3= titre,
            sous_titre= categorie_value,
            # trouvé une facon d'enregistrer l'image et l'afficher
            src_image_article= '../static/images/image_par_default.jpg',
            message= description,
            routes=lister_routes()
        )
    else:
        return render_template(
            'formulaire.jinja',
            routes=lister_routes()
        )

@app.route('/details_objet')
def liste_article():
    """Page d'index"""
    return render_template(
        'article.jinja',
        titre_h1='Bonjour!',
        message='Bienvenu sur la démo des template!',
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
            result = curseur.fetchone()
            if result:
                return result[0]  # Renvoie l'ID de la catégorie trouvée
            else:
                # Si aucune correspondance n'est trouvée, vous pouvez choisir de retourner None ou générer une exception, par exemple :
                raise ValueError("Catégorie non trouvée")
