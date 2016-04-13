package Kruskal;

/**
 * @author Desmoulins Thibault
 * @author Lesecque Yorick
 */
public class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // Initialise le graphe avec la matrice contenue dans le fichier graphe.txt
        Graphes g = new Graphes("graphe.txt");


        /*
         * On applique la fermeture transitive pour obtenir la matrice montrant
         * les composantes fortement connexe du graphe
         */
        g.fermetureTransitive();
        

        try {
            // Affiche le chemin le plus court entre les points H et D
            g.dijkstra("H", "D");
            g.interpreteResultat();

            // Affiche le chemin le plus court entre les points B et H
            g.dijkstra("B", "H");
            g.interpreteResultat();

            // Affiche le chemin le plus court entre les points H et B
            g.dijkstra("H", "B");
            g.interpreteResultat();

            // Affiche le chemin le plus court entre les points E et H
            g.dijkstra("E", "H");
            g.interpreteResultat();

            // Affiche le chemin le plus court entre les points H et E
            g.dijkstra("H", "E");
            g.interpreteResultat();
            
        } catch (IndexOutOfBoundsException e) {
            System.out.println(e.getMessage());
        }

        // Appel de la fonction kruskal pour afficher l'arbre couvrant minimal
        g.kruskal();

        g.afficheListeAdjacence();
    }

}
