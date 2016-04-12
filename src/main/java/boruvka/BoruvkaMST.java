package boruvka;

import business.Graph;

/**
 * Created by lucas on 12/04/16.
 */
public class BoruvkaMST {

    private Graph graphWithAllEdges;
    private Graph mst;
    private int weightMst;

    public BoruvkaMST(Graph graphWithAllEdges) {
        this.graphWithAllEdges = graphWithAllEdges;
    }

    /**
     * Launch boruvka algorithm on the graph
     */
    public void processAlgorithm(){
        //tant que graphe n'est pas constitué d'un sommet
        while(graphWithAllEdges.getV() == 1){
            //on detruit les boucles (meme endpoint)
            graphWithAllEdges.deleteLoopEdges();
            //on detruit les aretes multiples
            graphWithAllEdges.deleteMultipleEdgesBetweenVertices();
        }
    }
}
