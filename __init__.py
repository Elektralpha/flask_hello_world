from flask import Flask                                                                                                                
from flask import render_template                                                                                                      
from flask import json                                                                                                                 
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/fr/')                                                                                                                     
def hello_world_fr():                                                                                                                  
    return "<h2>Bonjour tout le monde !</h2>" 
    
    @app.route('/test/')                                                                                                                     
def test1():                                                                                                                  
     conn = get_db_connection() 

# Création d'une nouvelle route pour la lecture de la BDD
@app.route('/lecture/')
def ReadBDD():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM livres').fetchall()
    conn.close()

    # Convertit la liste de livre en un format JSON
    json_posts = [{'id': post['id'], 'title': post['title'], 'content': post['auteur']} for post in posts]

    # Renvoie la réponse JSON
    return jsonify(posts=json_posts)

if __name__ == "__main__":                                                                                                             
  app.run(debug=True)
