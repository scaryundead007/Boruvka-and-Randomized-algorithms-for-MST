package business;

import utils.Randomizer;

import java.util.*;

/**
 * Created by lucas on 12/04/16.
 */
public class Graph {

    private int V; //nb sommet
    private int E; //nb arete
    private Map<Integer, List<Edge>> allVerticesWithEdges; //ensemble des arretes du graphe en fonction du sommet
    private List<Edge> allEdges;

    /**
     * Creation des sommets (aucune arete)
     * @param v
     */
    public Graph(int v) {
        V = v;
        this.E = 0;
        this.allVerticesWithEdges = new HashMap<>();
        this.allEdges = new ArrayList<>();
    }

    public Graph(int v, int e) {
        V = v;
        this.allVerticesWithEdges = new HashMap<>();
        this.allEdges = new ArrayList<>();
        for(int i = 0 ; i < e ; ++i){
            int[] verticesId = Randomizer.getDiffRandoms(0,v);
            int weight = Randomizer.getWeight();
            Edge newEdge = new Edge(verticesId[0], verticesId[1], weight);
            addEdge(newEdge);
        }
    }

    public int getV() {
        return V;
    }

    public int getE() {
        return E;
    }

    public void addEdge(Edge e) {
        int v = e.either();
        int w = e.other(v);
        if(checkVertex(v) && checkVertex(w)){
            //si le sommet contient deja une arrete on met a jour la liste
            if(allVerticesWithEdges.get(new Integer(v)) != null)
                allVerticesWithEdges.get(new Integer(v)).add(e);
            //sinon on crée une nouvelle entrée dans la map
            else {
                List<Edge> edges = new ArrayList<>();
                edges.add(e);
                allVerticesWithEdges.put(new Integer(v), edges);
            }
            if(allVerticesWithEdges.get(new Integer(w)) != null)
                allVerticesWithEdges.get(new Integer(w)).add(e);
                //sinon on crée une nouvelle entrée dans la map
            else {
                List<Edge> edges = new ArrayList<>();
                edges.add(e);
                allVerticesWithEdges.put(new Integer(w), edges);
            }
            allEdges.add(e);
            E++;
        }
    }

    /**
     * return the edges connected to the vertice
     * @param vertice
     * @return
     */
    public Iterable<Edge> getAdjacent(int vertice){
        return allVerticesWithEdges.get(new Integer(vertice));
    }

    public Iterable<Edge> getAllEdges() {
        return allEdges;
    }

    /**
     * check if the vertex is in the graph
     * @param vertex
     * @return
     */
    private boolean checkVertex(int vertex){
        return (vertex >= 0 && vertex < V);
    }

    @Override
    public String toString() {
        String intro = "Graph{" +
                "V=" + V +
                ", E=" + E +
                "}\n";
        for(Map.Entry<Integer,List<Edge>> entry : allVerticesWithEdges.entrySet()){
            intro += entry.getKey() + " : ";
            for(Edge e : entry.getValue()){
                intro += e.toString() + " ";
            }
            intro += "\n";
        }
        return intro;
    }

    public static void main(String[] args) {
        Graph g = new Graph(5,5);
        System.out.println(g.toString());
    }
}
