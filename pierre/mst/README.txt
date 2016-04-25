

graph/kruskal.py
  vertex et edge
  kruskal

graph/boruvka.py
  vertex et edge
  boruvka

graph/randmst.py
  vertex et edge
  algo randomise

graph/random.py
  generateur de graphe random
  calcul de composantes connexes pour eviter les graphes non connectes
    quand la proba est faible

run.py
  sans argument
    compare les cas de tests en dur
    compare des graphes random de taille 100, 200, ... 3200
  avec arguments
    lance la comparaison pour les graphes random de la taille N donnee en argument
    la proba des aretes va de 0.1 à 1 par pas de 0.1
    On fait tourner 10 fois par graphe genere
    Par ex.
        ./run.py 1000 2000 4000 8000

