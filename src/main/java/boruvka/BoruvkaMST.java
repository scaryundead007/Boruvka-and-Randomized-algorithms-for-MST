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
        int i = 0;
        while(graphWithAllEdges.getV() != 1){
            weightMst += applyBoruvkaStep(graphWithAllEdges, mst);
            i++;
        }
        System.out.println("nombre d'itérations : " + i);
    }

    /**
     * Apply one step of the boruvka algorithme on the graph
     * @param g
     */
    public static int applyBoruvkaStep(Graph g, Graph mst) {
       // System.out.println(g);
        int weight = 0;
        //on detruit les boucles (meme endpoint)
        g.deleteLoopEdges();
        //on detruit les aretes multiples
        g.deleteMultipleEdgesBetweenVertices();
        List<Vertice> allComponents = g.getAllVertices();
        Set<Edge> miniEdges = new HashSet<>();
        //System.out.println(allComponents);
        //System.out.println(g);
       // g.updateV();
       // System.out.println(g.getV());
        for (Vertice v : allComponents) {
            Edge e = g.minimumWeightForVertice(v);
            miniEdges.add(e);
        }
        //System.out.println(miniEdges);
        //System.out.println("size : " + miniEdges.size() + " next : " + miniEdges.iterator().next());
        for (Edge e : miniEdges) {
                //System.out.println(e);
                mst.addEdge(e);
                weight += e.getWeight();
                g.mergeVertices(e);
        }
        return weight;
    }

    public static void cleanGraph(Graph g){
        //on detruit les boucles (meme endpoint)
        g.deleteLoopEdges();
        //on detruit les aretes multiples
        g.deleteMultipleEdgesBetweenVertices();
    }

    public Graph getMst() {
        return mst;
    }

    public int getWeightMst() {
        return weightMst;
    }
}
