"""
TP1 web 3
"""
import re
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
            'nom': 'Ajout article'
        },
        {
            'route': '/details_objet',
            'nom': 'Liste'
        }
    ]

@app.route('/')
def index():
    """Affiche la page d'accueil"""
    return render_template(
        'base.jinja',
        titre_h1='Bonjour!',
        message='Bienvenu sur la démo des templates!',
        routes=lister_routes()
    )


@app.route('/ajout_article')
def article():
    """Page d'index"""
    return render_template(
        'formulaire.jinja',
        titre_h1='Bonjour!',
        message='Bienvenu sur la démo des templates!',
        routes=lister_routes()
    )

@app.route('/details_objet')
def article():
    """Page d'index"""
    return render_template(
        'base.jinja',
        titre_h1='Bonjour!',
        message='Bienvenu sur la démo des templates!',
        routes=lister_routes()
    )

