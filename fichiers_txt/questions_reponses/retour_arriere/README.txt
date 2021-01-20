Ici on trouve les phrases utilisées lorsque le locuteur a besoin de retourner en arrière.
Le cas typique d'utilisation est lorsque une précision est faite alors que son type de lien
est prioritaire sur celui du lien principal. Si on ne revient pas au coeur actuel on ne comprends pas les liens.
"[]" est remplacé par le coeur actuel

### Il n'y a pas besoin de le faire pour les compléments car ils ne peuvent pas être choisis en liens principaux
### Les fichiers existent tout de même et sont vide pour faciliter le programme d'importation des fichiers textes


Exemple:
- CoeurActuel(Voiture, ecraser, chien)
- Precision: suite = (Marcel et chien, aller chez, veterinaire)
- LienChoisi: consequence = (Marcel, colère)

Si on effectue pas de retour en arrière, on obtient:
Une voiture écrase mon chien donc nous allons consulter un vétérinaire. Et du coup je suis plutot en colère.
===> On a l'impression que Marcel est en colère d'aller chez le véterinaire.

Ainsi, on fait un retour en arrière et on obtient:
Une voiture écrase mon chien donc nous allons consulter un vétérinaire. Comme une voitue écrase mon chien, je suis plutot en colère.
===> avec le retour en arriere: Comme [],