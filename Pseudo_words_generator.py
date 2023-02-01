from random import choices
import os
import codecs
import pickle
import unicodedata


def analyse(lexique, profondeur_max):
	
	proba_longeur = {}

	len_max = 0
	for mot in lexique:
		lm = len(mot)
		proba_longeur[lm] = proba_longeur.get(lm,0) + 1
		if lm > len_max: len_max = lm

	proba_debut = {i:{} for i in range(len_max)}
	proba_fin = {i:{} for i in range(len_max)}

	for mot in lexique:

		lm = len(mot)
		precedent = ''

		for profondeur in range(1,profondeur_max+1):

			for i,c in enumerate(mot):

				proba_debut[i][precedent] = proba_debut[i].get(precedent,{})
				proba_debut[i][precedent][c] = proba_debut[i][precedent].get(c,0) + 1
				proba_fin[inv][precedent] = proba_fin[inv := lm-i-1].get(precedent,{})
				proba_fin[inv][precedent][c] = proba_fin[inv][precedent].get(c,0) + 1

				precedent = precedent[(1,0)[len(precedent) < profondeur]:] + c

	probas = proba_longeur, proba_debut, proba_fin
	with open(local_path + f'/Data/Probas_gen_mots_3.0_{language}.pkl', 'wb') as f:
		pickle.dump(probas, f)


def genere(language, lexique, profondeur, nombre, longueur=0):

	with open(local_path + f'/Data/Probas_gen_mots_3.0_{language}.pkl', "rb") as file:
	    probas = pickle.load(file)

	proba_longueur, proba_debut, proba_fin = probas
	choix = lambda d: choices(list(d.keys()),weights=list(d.values()),k=1)[0]

	for i in range(nombre):

		l = longueur or choix(proba_longueur)
		fin = l//2
		debut = l-fin
		mot = ''
		dec = 0
		if int(profondeur) != profondeur: 
			mul = profondeur - int(profondeur)
			profondeur = int(profondeur) + 1
			dec = 1

		for rg, proba in ((range(debut), proba_debut),(range(fin-1,-1,-1), proba_fin)):
			for i in rg:
				precedent = mot[-(min(len(mot),profondeur)):]
				while precedent not in proba[i]:
					print("    --  baisse")
					precedent = precedent[1:]
				if dec and len(precedent) > profondeur:
					d = {k:v*mul for k,v in proba[i][precedent]}
					for k,v in proba[i][precedent[1:]]:
						d[k] = d.get(v,0) + v*(1-mul)
				else:
					d =  proba[i][precedent]
				mot += choix(d)

		if mot in lexique:
			genere(language, lexique, profondeur, 1, longueur=l)
		else:
			print(mot)


local_path = os.path.dirname(__file__)
fr = 'liste.de.mots.francais.frgut.txt'
en = 'English_words_alpha_370k.txt'
ru = 'Mots_russes.txt'
ro = 'Mots_roumains_180k.txt'
de = 'Mots_Allemands_344k.txt'
fi = 'Mots_finlandais_287k.txt'
hr = 'words.croatian.txt'
dk = 'words.danish.txt'
nl = 'words.dutch.txt'
it = 'words.italian.txt'
la = 'words.latin.txt'
no = 'words.norwegian.txt'
pl = 'words.polish.txt'


language = fr

with codecs.open(local_path + '/Data/' +  language, "r", "utf-8") as file:
	lexique = set(unicodedata.normalize('NFC', w.strip()) for w in file.readlines())

if not os.path.isfile(f"Data/Probas_gen_mots_3.0_{language}.pkl"):
	# création des probas, à la première utilisation
	print("Please wait, probas are being processed...")
	probas = analyse(lexique,3)

taille_des_mots = 0
profondeur = 2.12
nombre_de_mots = 20
mot = genere(language, lexique, profondeur, nombre_de_mots, taille_des_mots)
