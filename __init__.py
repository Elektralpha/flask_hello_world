from flask import Flask, render_template_string, render_template, jsonify
from flask import json
from urllib.request import urlopen
from flask import render_template   
from flask import jsonify
import sqlite3

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

# Définition de la fonction pour obtenir la connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Permet de récupérer les résultats sous forme de dictionnaire
    return conn
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/fr/')
def hello_world_fr():
    return "<h2>Bonjour tout le monde !</h2>"

@app.route('/EntreeDonnee/')
def Donnee():
    return "<h2>donne11</h2>"

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)



@app.route('/post/<int:post_id>')
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM livres WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    # Si la publication avec l'ID spécifié n'est pas trouvée, renvoie une réponse 404 Not Found
    if post is None:
        return jsonify(error='Post not found'), 404

    # Convertit la publication en un format JSON
    json_post = {'id': post['id'], 'title': post['title'], 'auteur': post['auteur']}
    
    # Renvoie la réponse JSON
    return jsonify(post=json_post)
  
@app.route('/lecture/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres;')
    data = cursor.fetchall()
    conn.close()

   # Construisez dynamiquement une chaîne de modèle HTML
    template_string = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Bibliotheque</title>
    </head>
    <body>
        <h1>Contenu de la base de données</h1>
        <table border="1">
            <tr>
                <th>ID</th>
                <th>DATE</th>
                <th>TITRE</th>
                <th>AUTEUR</th>
            </tr>
            {% for row in data %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(template_string, data=data)
                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)
