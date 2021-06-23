from flask import *
import psycopg2
import psycopg2.extras
from flask import Flask, render_template 

#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)

#Connection
# Try to connect to an existing database
USERNAME="engbamekoyap" # ID num :  21927314
try: # database: nom de la base de données, user: nom de l'utilisateur, password: mot de passe qui permet d'accéder  la BDD
  conn = psycopg2.connect(database=USERNAME, user=USERNAME,host='localhost', password='1234')
except Exception as e : #Lorsque l'accès à la BDD est réfusé pour une raison quelconque alors on devra afficher un message
  exit("Connexion impossible à la base de données: ", e)
#préparation de l'exécution des requêtes (à ne faire qu'une fois)
#En utilisant connection.cursor (), nous pouvons créer un objet curseur qui nous permet d'exécuter la commande PostgreSQL via le code source Python.
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

command = 'SELECT dragon FROM dragons;' # Recuperation du nom de dragon saisi
command1 = 'SELECT produit from Repas where repas.dragon=dragon;'
command2 = 'SELECT dragonaimant from Amours where dragonaime=%s'
try:
  cur.execute(command) # Requête sql reliant toutes les tables
except Exception as e :
  #fermeture de la connexion
  cur.close()
  conn.close()
  exit("error when running: " + command1 + " : " + str(e))    
liste_dragon = cur.fetchone()

try:
  cur.execute(command) # Requête sql reliant toutes les tables
except Exception as e :
  #fermeture de la connexion
  cur.close()
  conn.close()
  exit("error when running: " + command1 + " : " + str(e))    
liste_regime = cur.fetchall() # Liste des noms des regimes
try:
  cur.execute(command) # Requête sql reliant toutes les tables
except Exception as e :
  #fermeture de la connexion
  cur.close()
  conn.close()
  exit("error when running: " + command1 + " : " + str(e))    
liste_pretendants = cur.fetchall() # Liste des noms des regimes
########################################################################################################

#Cette partie permet de faire un traitement des valeurs saisie par l'utilisateur 
@app.route("/")
def accueil():
  return render_template("form2.html")
@app.route("/home")
def dragon_saisi():
  nom_dragon = request.args.get('input_dragon') # recupère le nom de dragon saisi
  test_pretendant = request.args.get('pretendant')!=None # test si le checkbox est coché ou pas
  test_regime = request.args.get('regime')!=None # test si le checkbox est coché ou pas
  # Exécution et récupération des informations
  if(test_regime == False):
    liste_pretendant = "pas choisi"
  if(test_pretendant == False):
    liste_regime = "pas choisis"
  for i in liste_dragon:
    if nom_dragon == i:
      return render_template("affichage.html",liste_pretendant = liste_pretendant, liste_regime = liste_regime)
  return redirect(url_for('error_dragon', error="le dragon n'existe pas")) # Retourne un message d'erreur au cas contraire

#Cette fonction nous permet de detecter l'erreur et renvoyer un message d'erreur
@app.route("/error_dragon")
def error_dragon():
  error = request.args.get('error')
  return render_template("form2.html", Error=error) 

#Cette fonction nous permet d'afficher la liste des dragons
@app.route('/dragonsListe')
def dragon_liste():
  dragons = ''
  for c in liste_dragon: #pour chaque entrée du tableau liste
    dragons += c['dragon']+"</br>" #la variable c est un dictionnaire pour chaque dragon. On veut les données associées à la 'dragon'
  return "<b>La liste complète des dragons :</b></br></br>"+dragons+"</br><a href='/'>retour au menu</a>
#-----------------------------------------------------------------------------------
#fermeture de la connexion
cur.close()
conn.close()

#NE SURTOUT PAS MODIFIER     
if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=5000)

# test : http://0.0.0.0:5000/
