#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
import json
import mysql.connector

# Créer l'objet Application Flask (Serveur)
app = Flask( __name__ )	

# Obtenir une connexion au SGBDR
connexionBD = mysql.connector.connect(
			host = 'localhost' ,
			user = 'root' ,
			password = 'azerty' ,
			database = 'GsbCRSlamV2015'
			#database = 'foody'
		)

# Page d'accueil
@app.route( '/' )
def accueil() :
	# Retourne un simple message (texte brut)
	return "GSB Services web"

# Liste des livreurs
#@app.route( '/livreurs' , methods=['GET'] )
#def getLivreurs() :
	# Obtenir un curseur
	#curseur = connexionBD.cursor()
	# Exécuter la requête
	#curseur.execute( 'select id,nom,prenom from Livreur' )
	# Lire tous les tuples qui résultent de l'exécution de la requête
	#tuples = curseur.fetchall()
	# Fermer le curseur
	#curseur.close()
	# Créer une liste vide de livreurs
	#livreurs = []
	# Parcourir tous les tuples qui résultent de l'exécution de la requête
	#for unTuple in tuples :
		# Convertir le tuple en dictionnaire (tableau associatif)
		#unLivreur = { 'id': unTuple[0] , 'nom': unTuple[1] , 'prenom': unTuple[2] }
		# Ajouter le dictionnaire dans la liste des livreurs
		#livreurs.append( unLivreur )
	
	# Convertir la liste des livreurs en chaîne au format JSON
	#reponse = json.dumps( livreurs )
	#print "Livreurs : " + reponse
	# Renvoyer la réponse au client HTTP
	#return Response( reponse , status=200 , mimetype='application/json' ) 





#Se connecter
@app.route( '/connexion/<idVisiteur>/<mdpVisiteur>' , methods=['GET'] )
def getConnexion( idVisiteur , mdpVisiteur ) :
	
	#obtenir un cursor
	curseur = connexionBD.cursor()
	#Exécuter la requete
	curseur.execute( 'select VIS_MATRICULE,VIS_NOM,VIS_PRENOM,VIS_MDP from VISITEUR where VIS_MATRICULE = \'' + idVisiteur + '\' and VIS_MDP = \'' + mdpVisiteur + '\'')
	#curseur.execute( 'select VIS_MATRICULE,VIS_MDP from VISITEUR where VIS_MATRICULE = ' + idVisiteur +'')
	tuples = curseur.fetchall()
	curseur.close()
	visiteurs = []
	for unTuple in tuples :
		unVisiteur = { 'VIS_MATRICULE': unTuple[0] , 'VIS_NOM': unTuple[1] ,  'VIS_PRENOM': unTuple[2] , 'VIS_MDP': unTuple[3] }
		visiteurs.append( unVisiteur )
	reponse = json.dumps( visiteurs )
	print "Visiteur : " + reponse
	return Response( reponse, status=200 , mimetype='application/json' )
	
	
	
	
#Liste des RV en rapport avec un Visiteur,un Mois, une Annee
@app.route( '/rv/<idVisiteur>/<moisRV>/<anneeRV>' , methods=['GET'] )
def getRapportVisite( idVisiteur, moisRV, anneeRV ) :
	
	curseur = connexionBD.cursor()
	curseur.execute( 'select VISITEUR.VIS_MATRICULE,VIS_NOM,MONTH(RAP_DATE), YEAR(RAP_DATE), DAY(RAP_DATE), RAP_BILAN, RAP_CONF from VISITEUR inner join RAPPORT_VISITE on VISITEUR.VIS_MATRICULE = RAPPORT_VISITE.VIS_MATRICULE where VISITEUR.VIS_MATRICULE = \'' + idVisiteur + '\' and MONTH(RAP_DATE) = '+ moisRV +' and YEAR(RAP_DATE) = ' + anneeRV + '')
	tuples = curseur.fetchall()
	curseur.close()
	rapportVisites = []
	for unTuple in tuples :
		unRapportVisite = { 'VISITEUR': unTuple[0] , 'VIS_NOM': unTuple[1] , 'MONTH(RAP_DATE)': unTuple[2] , 'YEAR(RAP_DATE)': unTuple[3], 'DAY(RAP_DATE)': unTuple[4], 'RAP_BILAN': unTuple[5], 'RAP_CONF': unTuple[6] }
		rapportVisites.append( unRapportVisite )
	reponse = json.dumps( rapportVisites )
	print "RapportVisite : " + reponse
	return Response( reponse, status=200 , mimetype='application/json' )

	


# Lire un livreur
#@app.route( '/livreurs/<idLivreur>' , methods=['GET'] )
#def getLivreur( idLivreur ) :
	
	# Votre code ici
	# Obtenir un curseur
	#curseur = connexionBD.cursor()
	# Exécuter la requête
	#curseur.execute( 'select id,nom,prenom from Livreur where id = ' + idLivreur + '' )
	# Lire tous les tuples qui résultent de l'exécution de la requête
	#tuples = curseur.fetchall()
	# Fermer le curseur
	#curseur.close()
	# Créer une liste vide de livreurs
	#livreurs = []
	# Parcourir tous les tuples qui résultent de l'exécution de la requête
	#for unTuple in tuples :
		# Convertir le tuple en dictionnaire (tableau associatif)
		#unLivreur = { 'id': unTuple[0] , 'nom': unTuple[1] , 'prenom': unTuple[2] }
		# Ajouter le dictionnaire dans la liste des livreurs
		#livreurs.append( unLivreur )
	
	# Convertir la liste des livreurs en chaîne au format JSON
	#reponse = json.dumps( livreurs )
	#print "Livreurs : " + reponse
	# Renvoyer la réponse au client HTTP
	#return Response( reponse , status=200 , mimetype='application/json' ) 
	
	
	
	
# Créer un rapportVisite
@app.route( '/rv/<VIS_MATRICULE>/<RAP_NUM>/<PRA_NUM>/<RAP_BILAN>/<RAP_DATE>/<RAP_CONF>' , methods=['PUT'] )
def addRapportVisite(VIS_MATRICULE,RAP_NUM,PRA_NUM,RAP_BILAN,RAP_DATE,RAP_CONF) :
	# Lire et mémoriser le corps de la requête (rapport sous la forme d'une chaîne JSON)
	unRapportJSON = request.data
	# Convertir la chaîne JSON en dictionnaire
	unRapport = json.loads( unRapportJSON )
	print unRapport
	
	# Obtenir un curseur
	curseur = connexionBD.cursor()
	# Exécuter la requête
	#curseur.execute( 'insert into RAPPORT_VISITE(VIS_MATRICULE,RAP_NUM,PRA_NUM,RAP_BILAN,RAP_DATE,RAP_CONF) values(%s,%s,%s,%s,%s,%s)' ,
	#( unRapport['VIS_MATRICULE'] , unRapport['RAP_NUM'] , unRapport['PRA_NUM'] , unRapport['RAP_BILAN'] , unRapport['RAP_DATE'] , unRapport['RAP_CONF'] ) )
	#curseur.execute( 'insert into RAPPORT_VISITE values(
	
	# Obtenir le dernier identifiant attribué
	idNouveauRapport = curseur.lastrowid
	# Obtenir le nombre de tuples insérés (normallement, un seul)
	nbTuplesTraites = curseur.rowcount
	# S'assurer que la BD est mise à jour
	connexionBD.commit()
	# Fermer le curseur
	curseur.close()
	
	# Créer un objet réponse
	reponse = make_response( '' )
	# Si l'insertion du rapport s'est déroulée avec succès
	if nbTuplesTraites == 1 :
		reponse.mimetype = 'text/plain'
		reponse.status_code = 201
		reponse.location = '/rv/' + str( idNouveauRapport )
		
	# Dans le cas contraire
	else :
		# Votre code ici
		
		reponse.mimetype = 'text/plain'
		reponse.status_code = 409
		reponse.location = '/rv/' + str( idNouveauRapport )
		
		
		
		
	return reponse	
	
	









	
	
# Créer un livreur
@app.route( '/livreurs' , methods=['PUT'] )
def addLivreur() :
	# Lire et mémoriser le corps de la requête (livreur sous la forme d'une chaîne JSON)
	unLivreurJSON = request.data
	# Convertir la chaîne JSON en dictionnaire
	unLivreur = json.loads( unLivreurJSON )
	print unLivreur
	
	# Obtenir un curseur
	curseur = connexionBD.cursor()
	# Exécuter la requête
	curseur.execute( 'insert into Livreur(nom,prenom) values(%s,%s)' , ( unLivreur['nom'] , unLivreur['prenom'] ) )
	# Obtenir le dernier identifiant attribué
	idNouveauLivreur = curseur.lastrowid
	# Obtenir le nombre de tuples insérés (normallement, un seul)
	nbTuplesTraites = curseur.rowcount
	# S'assurer que la BD est mise à jour
	connexionBD.commit()
	# Fermer le curseur
	curseur.close()
	
	# Créer un objet réponse
	reponse = make_response( '' )
	# Si l'insertion du livreur s'est déroulée avec succès
	if nbTuplesTraites == 1 :
		reponse.mimetype = 'text/plain'
		reponse.status_code = 200
		reponse.location = '/livreurs/' + str( idNouveauLivreur )
		
	# Dans le cas contraire
	else :
		# Votre code ici
		pass
		reponse.mimetype = 'text/plain'
		reponse.status_code = 404
		#reponse.location = '/livreurs/' + str( idNouveauLivreur )
		
		
		
		
	return reponse

# supprimer un livreur
#@app.route( '/livreurs/<idLivreur>' , methods=['DELETE'] )
def getLivreur( idLivreur ) :
	
	# Votre code ici
	# Obtenir un curseur
	curseur = connexionBD.cursor()
	# Exécuter la requête
	curseur.execute( 'Delete from Livreur where id = '+ idLivreur + '' )
	# Obtenir le dernier identifiant attribué
	idNouveauLivreur = curseur.lastrowid
	# Obtenir le nombre de tuples insérés (normallement, un seul)
	nbTuplesTraites = curseur.rowcount
	# S'assurer que la BD est mise à jour
	connexionBD.commit()
	# Fermer le curseur
	curseur.close()
	
	# Créer un objet réponse
	reponse = make_response( '' )
	# Si l'insertion du livreur s'est déroulée avec succès
	if nbTuplesTraites == 1 :
		reponse.mimetype = 'text/plain'
		reponse.status_code = 201
		reponse.location = '/livreurs/' + str( idNouveauLivreur )
		
	# Dans le cas contraire
	else :
		# Votre code ici
		
		reponse.mimetype = 'text/plain'
		reponse.status_code = 409
		reponse.location = '/livreurs/' + str( idNouveauLivreur )
		
		
		
		
	return reponse








# Programme principal
if __name__ == "__main__" :
	# Démarrer le serveur
	app.run( debug = True , host = '0.0.0.0' , port = 5000 )
