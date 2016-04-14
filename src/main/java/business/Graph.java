package business;

import boruvka.BoruvkaMST;
import utils.Randomizer;

import java.util.*;

/**
 * Created by lucas on 12/04/16.
 */
public class Graph implements Cloneable {

    private int V; //nb sommet
    private int E; //nb arete
    private Map<Vertice, List<Edge>> allVerticesWithEdges; //ensemble des arretes du graphe en fonction du sommet
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
            Edge newEdge = new Edge(new Vertice(verticesId[0]), new Vertice(verticesId[1]), weight);
            addEdge(newEdge);
        }
    }

    public int getV() {
        return V;
    }

    public int getE() {
        return E;
    }

    @Override
    public Graph clone() throws CloneNotSupportedException {
        Graph graph = new Graph(V);
        graph.setE(E);
        Map<Vertice, List<Edge>> newMap = new HashMap<>(allVerticesWithEdges);
        /*for(Map.Entry<Vertice,List<Edge>> entry : allVerticesWithEdges.entrySet()){
            newMap.put(entry.getKey().clone())
        }*/
        graph.setAllVerticesWithEdges(newMap);
        List<Edge> newEdges = new ArrayList<>(allEdges);
        //newEdges.addAll(allEdges);
        graph.setAllEdges(newEdges);
        return graph;
    }

    public void addEdge(Edge e) {
        Vertice v = e.either();
        Vertice w = e.other(v);
        //if(checkVertex(v) && checkVertex(w)){
            //si le sommet contient deja une arrete on met a jour la liste
            if(allVerticesWithEdges.get(v) != null)
                allVerticesWithEdges.get(v).add(e);
            //sinon on crée une nouvelle entrée dans la map
            else {
                //System.out.println(allVerticesWithEdges.get(v));
                List<Edge> edges = new ArrayList<>();
                edges.add(e);
                allVerticesWithEdges.put(v, edges);
                //System.out.println(allVerticesWithEdges.get(v));
            }
            if(allVerticesWithEdges.get(w) != null)
                allVerticesWithEdges.get(w).add(e);
                //sinon on crée une nouvelle entrée dans la map
            else {
                List<Edge> edges = new ArrayList<>();
                edges.add(e);
                allVerticesWithEdges.put(w, edges);
            }
            allEdges.add(e);
            E++;
        //}
    }

    /**
     * remove the edges in the graph
     * @param edges
     */
    public void deleteListEdges(List<Edge> edges){
        for(Edge e : edges){
            allEdges.remove(e);
            for(Map.Entry<Vertice,List<Edge>> entry : allVerticesWithEdges.entrySet()){
                entry.getValue().remove(e);
            }
            E--;
        }
    }

    /**
     * return the edges connected to the vertice
     * @param vertice
     * @return
     */
    public Iterable<Edge> getAdjacent(Vertice vertice){
        return allVerticesWithEdges.get(vertice);
    }

    public Iterable<Edge> getAllEdges() {
        return allEdges;
    }

    /**
     * check if the vertex is in the graph
     * @param vertex
     * @return
     */
    private boolean checkVertex(Vertice vertex){
        return (vertex.getNb() >= 0 && vertex.getNb() < V);
    }

    /**
     * check if the vertice exists
     * @param vertice
     * @return
     */
    public boolean checkExistVertice(Vertice vertice){
        for(Map.Entry<Vertice,List<Edge>> entry : allVerticesWithEdges.entrySet()){
            if(entry.getKey().equals(vertice))
                return true;
        }
        return false;
    }

    /**
     * delete edges with the same endpoint (v == w)
     */
    public void deleteLoopEdges(){
        //suppression du graphe
        for(Map.Entry<Vertice,List<Edge>> entry : allVerticesWithEdges.entrySet()){
            Iterator<Edge> it = entry.getValue().iterator();
            while(it.hasNext()){
                Edge e = it.next();
                if(e.either() == e.other(e.either()))
                    it.remove();
            }
        }
        //suppression de la list
        Iterator<Edge> it = allEdges.iterator();
        while(it.hasNext()){
            Edge e = it.next();
            if(e.either() == e.other(e.either())){
                it.remove();
                E--;
            }
        }
    }

    /**
     * Remove an edge if another one connect the same endpoint with a lower weight
     */
    public void deleteMultipleEdgesBetweenVertices(){
        List<Edge> toRm = new ArrayList<>();
        for (int i = 0; i < allEdges.size(); i++) {
            if(toRm.contains(i)) continue;
            for (int j = i+1; j < allEdges.size(); j++) {
                if(allEdges.get(i).sameEdge(allEdges.get(j))) {
                    if (allEdges.get(i).getWeight() < allEdges.get(j).getWeight()) {
                        toRm.add(allEdges.get(j));
                    } else if (allEdges.get(i).getWeight() > allEdges.get(j).getWeight()) {
                        toRm.add(allEdges.get(i));
                        break;
                    }
                }
            }
        }
        deleteListEdges(toRm);
    }

    /**
     * Return all the vertices in the graph
     * @return
     */
    public List<Vertice> getAllVertices(){
        List<Vertice> allVertices = new ArrayList<>();
        for(Map.Entry<Vertice,List<Edge>> entry : allVerticesWithEdges.entrySet()){
            allVertices.add(entry.getKey());
        }
        return allVertices;
    }

    /**
     * Return the edge with the minimum weight connected to the vertice
     * @param v
     * @return
     */
    public Edge minimumWeightForVertice(Vertice v){
        List<Edge> edgesForVertice = allVerticesWithEdges.get(v);
        Edge min = null;
       // System.out.println("nb sommet : " + v.getNb() + "size" + edgesForVertice.size());
        for(Edge e : edgesForVertice){
            if(min == null || e.getWeight() < min.getWeight()){
                min = e;
            }
        }
        return min;
    }

    /**
     * Concat the vertices for the edge in param
     * @param e
     */
    public void mergeVertices(Edge e){
        Vertice finalVert = e.either();
        Vertice rmvert = e.other(finalVert);
        for(Map.Entry<Vertice,List<Edge>> entry : allVerticesWithEdges.entrySet()){
            if(entry.getKey().equals(finalVert)){
                entry.getValue().addAll(allVerticesWithEdges.get(rmvert));
            }

            for(Edge ed : entry.getValue()){
                if(ed.either().equals(rmvert))
                    ed.setV(finalVert);
                if(ed.other(ed.either()).equals(rmvert))
                    ed.setW(finalVert);
            }
        }
        allVerticesWithEdges.remove(rmvert);
        V--;
    }

    /**
     * Update the number of vertice
     */
    public void updateV(){
        int cpt = 0;
        for(Map.Entry<Vertice,List<Edge>> entry : allVerticesWithEdges.entrySet()){
            ++cpt;
        }
        V = cpt;
    }

    /**
     * Return the weight of the heaviest edge
     * @return
     */
    public int getMaxWeight(){
        Edge max = new Edge(new Vertice(0), new Vertice(0),0);
        for(Edge e : allEdges){
            if(max.getWeight() < e.getWeight())
                max = e;
        }
        return max.getWeight();
    }

    @Override
    public String toString() {
        String intro = "Graph{" +
                "V=" + V +
                ", E=" + E +
                "}\n";
        for(Map.Entry<Vertice,List<Edge>> entry : allVerticesWithEdges.entrySet()){
            intro += entry.getKey().toString() + " : ";
            for(Edge e : entry.getValue()){
                intro += e.toString() + " ";
            }
            intro += "\n";
        }
        return intro;
    }

    public String toStringInit(){
        String intro = "Graph{" +
                "V=" + V +
                ", E=" + E +
                "}\n";
        for(Map.Entry<Vertice,List<Edge>> entry : allVerticesWithEdges.entrySet()){
            intro += entry.getKey().toString() + " : ";
            for(Edge e : entry.getValue()){
                intro += e.toStringInit() + " ";
            }
            intro += "\n";
        }
        return intro;
    }

    public void setE(int e) {
        E = e;
    }

    public void setAllVerticesWithEdges(Map<Vertice, List<Edge>> allVerticesWithEdges) {
        this.allVerticesWithEdges = allVerticesWithEdges;
    }

    public void setAllEdges(List<Edge> allEdges) {
        this.allEdges = allEdges;
    }

    public static void main(String[] args) {
        //Graph g = new Graph(5,5);
        //g.addEdge(new Edge(new Vertice(4),new Vertice(4),7));
        //System.out.println(g.toString());
        /*g.deleteLoopEdges();
        System.out.println(g.toString());
        Edge e = new Edge(new Vertice(4),new Vertice(3),5);
        g.addEdge(new Edge(new Vertice(4),new Vertice(3),7));
        g.addEdge(new Edge(new Vertice(3),new Vertice(4),6));
        g.addEdge(e);
        System.out.println(g.toString());
        g.deleteMultipleEdgesBetweenVertices();
        System.out.println(g.toString());
        g.mergeVertices(e);
        System.out.println(g.toString());*/
        Graph bis = new Graph(6);
        bis.addEdge(new Edge(new Vertice(0), new Vertice(1), 10));
        bis.addEdge(new Edge(new Vertice(0), new Vertice(2), 12));
        bis.addEdge(new Edge(new Vertice(0), new Vertice(3), 9));
        bis.addEdge(new Edge(new Vertice(1), new Vertice(3), 10));
        bis.addEdge(new Edge(new Vertice(1), new Vertice(2), 8));
        bis.addEdge(new Edge(new Vertice(2), new Vertice(3), 11));
        bis.addEdge(new Edge(new Vertice(4), new Vertice(0), 7));
        bis.addEdge(new Edge(new Vertice(4), new Vertice(2), 6));
        bis.addEdge(new Edge(new Vertice(3), new Vertice(5), 5));
        bis.addEdge(new Edge(new Vertice(1), new Vertice(5), 3));
       // System.out.println(bis.toString());
        BoruvkaMST b = new BoruvkaMST(bis);
        b.processAlgorithm();
        System.out.println(bis.toString());
        Graph mst =  b.getMst();
        for(Edge e : mst.getAllEdges()){
            System.out.println(e.toStringInit());
        }
        System.out.println(b.getWeightMst());
    }
}
