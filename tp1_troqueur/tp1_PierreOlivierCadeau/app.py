"""
TP1 web 3
"""

from flask import Flask, render_template

app = Flask(__name__)

def lister_routes():
    """Liste les routes pour le menu"""
    return [
        {
            'route': '/',
            'nom': 'Accueil'
        },
        {
            'route': '/details_objet',
            'nom': 'Liste'
        }
    ]

@app.route('/')
def index():
    """Page d'index"""
    return render_template(
        'base.jinja',
        titre_h1='Bonjour!',
        message='Bienvenu sur la démo des templates!',
        routes=lister_routes()
    )

@app.route('/details_objet')
def detail():
    """Page d'index"""
    return render_template(
        'base.jinja',
        titre='Salut!',
        message='Bienvenu sur la démo des templates!',
        routes=lister_routes()
    )

