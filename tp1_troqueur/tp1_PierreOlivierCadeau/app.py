"""
TP1 web 3
"""
import re
import bd
from flask import Flask, render_template, request

app = Flask(__name__)

def lister_routes():
    """Liste les routes pour le menu"""
    return [
        {
            'route': '/',
            'nom': 'Accueil'
        },
        {
            'route': '/ajout_article',
            'nom': "Ajout d'un article"
        },
        {
            'route': '/details_objet',
            'nom': 'Tous les articles'
        }
    ]

@app.route('/')
def index():
    """Affiche la page d'accueil"""
    return render_template(
        'article.jinja',
        titre_h2='Les 5 derniers cas répertorié',
        titre_h3='Test',
        src_image_article= '../static/images/scp1471.jpg',
        message="Description d'article!",
        routes=lister_routes()
    )


@app.route('/ajout_article')
def ajout_article():
    """Page d'index"""
    return render_template(
        'formulaire.jinja',
        titre_h1='Bonjour!',
        message='Bienvenu sur la démo des templates!',
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


def insertion_objet(u_id, u_titre, u_description, u_photo, u_categorie, u_commentaires):
    """Pour démontrer une insertion"""

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            # Insertion de objet
            curseur.execute(
                "INSERT INTO `objets` " +
                "(`id`, `titre`, `description`, `photo`, `categorie`) " +
                "VALUES (" +
                "%(u_id)s, %(u_titre)s, %(u_description)s, %(u_photo)s, %(u_categorie)s, %(u_commentaires)s )"
            )

            print(f"Identifiant de l'élément ajouté : {curseur.lastrowid}")
