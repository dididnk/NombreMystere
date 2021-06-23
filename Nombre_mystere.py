from flask import *
import random

    
#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)
cpt = 3 #Global variable, le compteur qui permet de determiner le nombre de tentative
aleatoire = random.randint(0,100) #cette variable contient le nombre aléatoire
@app.route("/") #Page d'accueil
def traitement():
   error = request.args.get('error')#Permet de récuperer le message d'erreur
   nbEssaie = request.args.get('nbEssaie')#Permet de récuperer l'indice (le mot clé) qui va nous permettre d'exploiter le compteur
   global cpt #Mot clé pour appelé la variable global
   if nbEssaie == "perdu": #A chaque fois que l'utilisateur n'aura pas le nombre gagnant
      if cpt == "Votre dernière chance!": #Juste dans le cas oU le compteur sera égal à 1
         cpt = 1
      cpt = cpt-1 #On decrementera le nombre d'essaie
   if cpt == 1:
      cpt = "Votre dernière chance!" #Un petit message pour le plaisir
   if cpt == 0: #lorsque le nombre d'essaie sera égale à 0
      cpt = 10 #SI OUI, on Reinitialise le compteur
      return "<b>Perdu ! :(</b></br></br><a href='/'>retour au jeu</a>" #Si OUI, on afficher le message Perdu avec un lien pour rentrer au jeu
   return render_template("frm_jeux.html", hasError=error, nbEssaie=cpt) #Sinon on reste dans le jeu
@app.route("/home")
def traitement_1():
   chiffre = int(request.args.get('input_chiffre')) #Nous permet de récuperer le nombre saisi par l'utilisateur
   global aleatoire
   if chiffre < 0 or chiffre > 100: #Lorsque l'utilisateur aura saisi un nombre qui n'est pas dans [0, 100]
      return redirect(url_for('traitement', error="Veillez saisir un nombre Valide!"))   #On affichera un message d'erreur 
   elif chiffre == aleatoire: #Si l'utilisateur reussi
      return "<b>Gagné</b></br></br><a href='/'>Rejouer encore</a>" #On affiche, Gagné puis on il pourra cliqué sur le lien pour retenter
   elif chiffre > aleatoire : #Si le nombre saisi est plus grand que le nombre aléatoire
      return redirect(url_for('traitement', error="Trop Grand!", nbEssaie="perdu")) #On affiche Trop grand et on renvoie Perdu afin de decrementer le compteur (nombre d'essaie)
   if chiffre < aleatoire : #Si le nombre saisi est plus petit que le nombre aléatoire
      return redirect(url_for('traitement', error="Trop Petit!", nbEssaie="perdu")) #On affiche Trop petit et on renvoie Perdu afin de decrementer le compteur (nombre d'essaie)

#NE SURTOUT PAS MODIFIER     
if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port=5000)

# test : http://localhost:5000
