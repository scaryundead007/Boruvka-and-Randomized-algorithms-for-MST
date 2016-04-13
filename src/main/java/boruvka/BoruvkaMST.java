package boruvka;

import business.Edge;
import business.Graph;
import business.Vertice;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Created by lucas on 12/04/16.
 */
public class BoruvkaMST {

    private Graph graphWithAllEdges;
    private Graph mst;
    private int weightMst;

    public BoruvkaMST(Graph graphWithAllEdges) {
        this.graphWithAllEdges = graphWithAllEdges;
        this.mst = new Graph(graphWithAllEdges.getV());
    }

    /**
     * Launch boruvka algorithm on the graph
     */
    public void processAlgorithm(){
        //tant que graphe n'est pas constitué d'un sommet
        while(graphWithAllEdges.getV() != 1){
            //on detruit les boucles (meme endpoint)
            graphWithAllEdges.deleteLoopEdges();
            //on detruit les aretes multiples
            graphWithAllEdges.deleteMultipleEdgesBetweenVertices();
            List<Vertice> allComponents = graphWithAllEdges.getAllVertices();
            Set<Edge> miniEdges = new HashSet<>();
            for(Vertice v : allComponents){
                Edge e = graphWithAllEdges.minimumWeightForVertice(v);
                miniEdges.add(e);
            }
            for(Edge e : miniEdges){
                System.out.println(e);
            }
            System.out.println("Concat");
            for(Edge e : miniEdges){
                mst.addEdge(e);
                weightMst += e.getWeight();
                graphWithAllEdges.mergeVertices(e);
            }
            System.out.println(graphWithAllEdges);
        }
    }

    public Graph getMst() {
        return mst;
    }

    public int getWeightMst() {
        return weightMst;
    }
}
