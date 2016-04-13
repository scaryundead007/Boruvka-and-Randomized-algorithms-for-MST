package Kruskal;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

/**
 * @author Desmoulins Thibault
 * @author Lesecque Yorick
 */
public class Graphes {
    public int[][] graphe, tabPoids;
    public int[] tabAntecedents;
    public int dep, arrivee;
    public String[] corressNom;

    public Graphes(String nomFichier) {
        this.graphe = getGraphe(nomFichier);
    }

    /*
     * Ouvre le fichier passé en paramètre et initialise une matrice avec le contenu
     * du fichier. Il suffit donc juste de changer le fichier pour charger un nouveau
     * graphe.
     */
    private int[][] getGraphe(String nomFichier) {
        try {
            File fichier = new File(System.getProperty("user.dir") + "/" + nomFichier);
            FileReader fichierLire = new FileReader(fichier);
            BufferedReader buff = new BufferedReader(fichierLire);

            try {
                String l = buff.readLine();
                String[] s = l.split(";");
                corressNom = new String[s.length];
                System.arraycopy(s, 0, corressNom, 0, s.length);

                // Initialise le tableau
                int[][] graphe = new int[s.length][s.length];
                int i = 0, j = 0;

                l = buff.readLine();

                // Tant qu'il y a des lignes dans le fichier
                while(l != null) {
                    s = l.split(";"); // On découpe avec le ;
                    j = 0;

                    // Pour chaque poids
                    for(String p : s) {
                        int poids = Integer.parseInt(p);

                        if(poids != 0) {
                            graphe[i][j] = poids;
                        }

                        j++;
                    }

                    i++;

                    l = buff.readLine();
                }

                return graphe;

            } catch(IOException e) {
                    return null;
            }
        } catch(FileNotFoundException e) {
            System.out.println("Fichier non trouvé");
            return null;
        }
    }






    /* === DEBUT DES FONCTIONS POUR FERMETURE TRANSITIVE === */

        /* Initialise une matrice de taille n * n (chaque case contenant 0) */
        public int[][] getMatrice(int n) {
            int[][] nouvelle = new int[n][n];
            for(int i=0 ; i<n ; i++) {
                for(int j=0 ; j<n ; j++) {
                    nouvelle[i][j] = 0;
                }
            }
            return nouvelle;
        }

        /* Affiche la matrice passée en paramètre */
        public void afficheMatrice(int[][] matrice, String titre) {
            int n = matrice.length;

            System.out.println("=== " + titre + " ===");
            for(int i=0 ; i<n ; i++) {
                for(int j=0 ; j<n ; j++) {
                    System.out.print(matrice[i][j]+" ");
                }
                System.out.println("");
            }
            System.out.println("===============\n");
        }

        /* ET logique entre les 2 matrices */
        private int[][] getTransition(int[][] mPrecedent, int[][] mSuivant) {
            int n = mPrecedent.length;
            int[][] nouvelle = getMatrice(n);

            for(int i=0 ; i<n ; i++) {
                for(int j=0 ; j<n ; j++) {
                    for(int k=0 ; k<n ; k++) {
                        if(mPrecedent[i][k]!=0 && mSuivant[k][j]!=0) {
                            nouvelle[i][j] = 1;
                        }
                    }
                }
            }

            return nouvelle;
        }

        /* OU logique entre les 2 matrices */
        private int[][] getMChapeau(int[][] m0, int[][] m1) {
            int n = m0.length;
            int[][] nouvelle = getMatrice(n);

            for(int i=0 ; i<n ; i++) {
                for(int j=0 ; j<n ; j++) {
                    if(m0[i][j]!=0 || m1[i][j]!=0) {nouvelle[i][j] = 1;}
                    else {nouvelle[i][j] = 0;}
                }
            }

            return nouvelle;
        }

        /* Retourne true si les 2 matrices sont égales, false le cas échéant */
        private boolean matricesEgales(int[][] m1, int[][] m2) {
            int n = m1.length;

            for(int i=0 ; i<n ; i++) {
                for(int j=0 ; j<n ; j++) {
                    if(m1[i][j]!=m2[i][j]) {return false;}
                }
            }

            return true;
        }

        public void fermetureTransitive() {
            int[][] mChapeau1;
            int n = graphe.length;

            // Initialisation de la première matrice (matrice carrée)
            int[][] mNouvelle = getMatrice(n);
            for(int i=0 ; i<n ; i++) {mNouvelle[i][i] = 1;}

            // OU logique entre les 2 matrices (la matrice de base et la matrice carrée)
            int[][] mChapeau2 = getMChapeau(graphe, mNouvelle);

            mNouvelle = graphe;

            /* On calcule les matrices chapeau JUSQU'A ce que les résultats n'évoluent pas */
            int i = 1;
            do {
                // ET logique entre les 2 matrices
                mNouvelle = getTransition(graphe, mNouvelle);


                // On sauvegarde l'ancienne matrice chapeau pour la comparer à la nouvelle que l'on va calculer
                mChapeau1 = mChapeau2;


                // OU logique entre les 2 matrices (la précédente matrice et celle que l'on vient de calculer au dessus)
                mChapeau2 = getMChapeau(mChapeau1, mNouvelle);


                // On affiche la matrice intermédiaire pour voir le résultat (ligne à commenter si on le souhaite)
                afficheMatrice(mChapeau1, "Matrice intermédiaire");


                i++; // Une étape de +
                
            } while(!matricesEgales(mChapeau1, mChapeau2));

            // On affiche la matrice finale et son nombre d'étapes pour la calculer
            afficheMatrice(mChapeau2, "/!\\ Matrice finale /!\\");
            System.out.println("Fermeture transitive finie en "+i+" étapes\n");
        }

    /* === FIN DES FONCTIONS POUR FERMETURE TRANSITIVE === */





    /* === DEBUT DES FONCTIONS POUR DIJKSTRA === */

        private int getMinDistance(int[][] tabPoids) {
            int minDist = Integer.MAX_VALUE, index = -1;

            for(int i = 0; i < tabPoids.length; i++) {
                if(tabPoids[i][0] < minDist && tabPoids[i][0] >= 0 && nonVisite(tabPoids[i][1])) {
                   minDist = tabPoids[i][0];
                   index = i;
                }
            }

            return index;
        }

        private Boolean nonVisite(int tabPoids) {
            return (tabPoids == 0)?true:false;
        }

        private int[] getEnfants(int noeud) throws noChildException {
            int noChild = 0;

            for(int i : graphe[noeud]) {
                if(i != 0) {
                    noChild++;
                }
            }

            if(noChild == 0) { throw new noChildException(); }
            else {
                int childs[] = new int[noChild];
                int j = 0, i = 0;

                for(int m : graphe[noeud]) {
                    if(m != 0) {
                        childs[j] = i;
                        j++;
                    }

                    i++;
                }

                return childs;
            }
        }

        public void dijkstra(String ptDepart, String ptArrivee)
                throws IndexOutOfBoundsException {
            boolean a = false, d = false;

            for(int i = 0; i < corressNom.length; i++) {
                if(corressNom[i].compareToIgnoreCase(ptDepart) == 0) {
                    this.dep = i;
                    d = true;
                }

                if(corressNom[i].compareToIgnoreCase(ptArrivee) == 0) {
                    this.arrivee = i;
                    a = true;
                }
            }

            if(!a || !d) {
                throw new IndexOutOfBoundsException("Les points demandés n'existent pas.");
            }

            int[][] tabPoids = new int[graphe.length][2];
            int[] tabAntecedents = new int[graphe.length];
            int dernierAntecedent = -1;

            //initialisation des poids à -1 et 0 pour le point de départ
            for(int i = 0; i < tabPoids.length; i++) {
                if(i != dep) {
                    tabPoids[i][0] = -1;
                }
            }

            //initialisation des antécédents à -1 pour "aucun"
            for(int i = 0; i < tabAntecedents.length; i++) {
                tabAntecedents[i] = -1;
            }

            int i = dep;

            while(i != -1) {
                try {
                    int[] enfants = getEnfants(i);

                    for(int m : enfants) {
                        if(tabPoids[m][1] == 0) {
                            if(tabPoids[m][0] > tabPoids[i][0] + graphe[i][m] || tabPoids[m][0] == -1) {
                                tabPoids[m][0] = tabPoids[i][0] + graphe[i][m];
                                tabAntecedents[m] = i;
                                dernierAntecedent = i;
                            }
                        }
                    }

                    tabPoids[i][1] = 1;
                } catch (noChildException ex) {
                    tabAntecedents[i] = dernierAntecedent;
                    tabPoids[i][1] = 1;
                } finally {
                    i = getMinDistance(tabPoids);
                }
            }

            this.tabPoids = tabPoids;
            this.tabAntecedents = tabAntecedents;
        }

        public void interpreteResultat() {
            int i = tabAntecedents[arrivee], j = 0;
            String[] chemin = new String[tabAntecedents.length];
            chemin[j] = corressNom[arrivee];
            j++;

            System.out.println("\n=== Dijkstra : chemin le plus court de "+corressNom[dep]+" vers "+corressNom[arrivee]+" ===");
            System.out.print(corressNom[dep]);

            while(i != dep) {
                chemin[j] = corressNom[i];

                j++;
                i = tabAntecedents[i];
            }

            for(i = j - 1; i >= 0; i--) {
                System.out.print(" -> " + chemin[i]);
            }

            System.out.println(" et la distance est de " + tabPoids[arrivee][0]);
            System.out.println("=== FIN Dijkstra ===");
        }

    /* === FIN DES FONCTIONS POUR DIJKSTRA === */




    /* === DEBUT DES FONCTIONS POUR KRUSKAL === */

        public int getIndexMinPoids(int[] matrice) {
            int n       = matrice.length;
            int min     = Integer.MAX_VALUE;
            int index   = -1;

            for(int i=0 ; i<n ; i++) {
                if(matrice[i]>0 && matrice[i]<min) {
                    min   = matrice[i];
                    index = i;
                }
            }

            return index;
        }

        public void kruskal() {
            int n = graphe.length;
            int[] matrice = new int[n*n];
            int index = -2;
            int row, col, rowListe, colListe, rowIndex, colIndex;
            boolean pasBon;

            ArrayList<Integer> res = new ArrayList<Integer>();


            // Initialisation d'une matrice à une dimension à partir du graphe
            for(int i=0 ; i<n ; i++) {
                for(int j=0 ; j<n ; j++) {
                    matrice[(i*n)+j] = graphe[i][j];
                }
            }

            while(res.size()<n-1 || index==-1) {
                index = getIndexMinPoids(matrice);

                if(index>=0) {
                    rowIndex   = index/n; // La nouvelle matrice n'étant plus qu'à une dimension on retrouve sa ligne en divisant nb par n
                    colIndex   = index%n; // La nouvelle matrice n'étant plus qu'à une dimension on retrouve sa colone en prenant nb modulo
                    pasBon     = false;

                    for(Integer nb : res) {
                        rowListe = nb/n; // La nouvelle matrice n'étant plus qu'à une dimension on retrouve sa ligne en divisant nb par n
                        colListe = nb%n; // La nouvelle matrice n'étant plus qu'à une dimension on retrouve sa colone en prenant nb modulo n


                        if(colListe==colIndex && rowIndex!=rowListe) {
                            pasBon = true;
                        }

                        // Ne pas prendre A<->B ET B<->A
                        if(rowIndex==colListe && colIndex==rowListe) {
                            pasBon = true;
                        }
                    }

                    // Ne pas prendre A<->B ET B<->A
                    if(res.contains((colIndex*n)+rowIndex)) {
                        pasBon = true;
                    }

                    // On ajoute ce vecteur à la liste
                    if(!pasBon) { res.add(index); }

                    // On marque ce vecteur comme traité
                    matrice[index] = -1;
                }
            }


            // AFFICHAGE DU RESULTAT
            System.out.println("\n\n=== Kruscal : arbre couvrant minimal ===");
            for(int nb : res) {
                row = nb/n;
                col = nb%n;
                System.out.println("matrice["+row+"]["+col+"] - "+corressNom[row]+"->"+corressNom[col]);
            }
            System.out.println("=== FIN Kruscal ===");
        }

    /* === FIN DES FONCTIONS POUR KRUSKAL === */



    

    public ArrayList<ListeChainee> getListeAdjacence() {
        ArrayList<ListeChainee> liste = new ArrayList<ListeChainee>();
        int n = graphe.length;

        for(int i=0 ; i<n ; i++) {
            ListeChainee l = new ListeChainee(i);

            for(int j=0 ; j<n ; j++) {
                if(graphe[i][j]>0) {
                    l.addAdjacent(j);
                }
            }

            liste.add(l);
        }
        return liste;
    }

    public void afficheListeAdjacence() {
        // AFFICHAGE DU RESULTAT
        ArrayList<ListeChainee> liste = getListeAdjacence();
        System.out.println("\n\n=== Liste d'adjacence ===");
        for(ListeChainee l : liste) {
            System.out.print(corressNom[l.num]+" : ");
            int n = l.liste.size();
            for(int i=0 ; i<n ; i++) {
                System.out.print(corressNom[l.liste.get(i)]);
                if(i!=n-1) {
                    System.out.print(" > ");
                }
            }
            System.out.print("\n");
        }
        System.out.println("=== FIN Liste d'adjacence ===");
    }
}
