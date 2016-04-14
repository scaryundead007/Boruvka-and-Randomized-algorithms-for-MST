package randomized;

import boruvka.BoruvkaMST;
import business.Edge;
import business.Graph;
import business.Vertice;
import utils.Randomizer;

/**
 * Created by lucas on 14/04/16.
 */
public class RandomizedAlgo {

    private Graph graphWithAllEdges;
    private Graph mst;
    private int weightMst;

    public RandomizedAlgo(Graph graphWithAllEdges) {
        this.graphWithAllEdges = graphWithAllEdges;
        this.weightMst = 0;
    }

    public static Graph processRandomizedAlgo(Graph g) throws CloneNotSupportedException {
        if(g.getV() == 1)
            return g;
        Graph copyG = g.clone();
        Graph inter = new Graph(g.getV());
        Graph inter2 = new Graph(g.getV());
        /*Apply two septs of boruvka*/
        BoruvkaMST.applyBoruvkaStep(g, inter);
        //inter.updateV();
        if(g.getV() == 1)
            return inter;
        BoruvkaMST.applyBoruvkaStep(g, inter2);
        BoruvkaMST.cleanGraph(g);
        //inter2.updateV();
        Graph afterBoruvka = new Graph(inter.getV());
        for(Edge e : inter.getAllEdges())
            afterBoruvka.addEdge(e);
        for(Edge e : inter2.getAllEdges())
            afterBoruvka.addEdge(e);
        if(g.getV() == 1)
            return afterBoruvka;
        /*get mst of a subgraph chosen randomly*/
        /*get subgraph of mst*/
        Graph subGraph = new Graph(g.getV());
        while(subGraph.getE() == 0 ){
            for(Edge e : copyG.getAllEdges()){
                if(Randomizer.takeItOrNot())
                    subGraph.addEdge(e);
            }
        }
        subGraph.updateV();
        Graph f1 = new Graph(subGraph.getV());
        System.out.println(subGraph);
        f1 = processRandomizedAlgo(subGraph);
        System.out.println("after f1");
        f1.updateV();
        Graph g2 = new Graph(g.getV());
        int maxWeight = f1.getMaxWeight();
        for(Edge e : copyG.getAllEdges()){
            if(e.getWeight() < maxWeight)
                g2.addEdge(e);
        }
        g2.updateV();
        if(g2.getV() == 0) {
            return afterBoruvka;
        }
        Graph f2 = new Graph(subGraph.getV());
        System.out.println("max weight " + maxWeight + " g2 " + g2);
        f2 = processRandomizedAlgo(g2);
        f2.updateV();
        System.out.println("apres f2");
        Graph union = new Graph(g.getV());
        for(Edge e : f2.getAllEdges())
            union.addEdge(e);
        for(Edge e : afterBoruvka.getAllEdges())
            union.addEdge(e);
        return union;
    }

    /**
     * First Recursion F1
     * @param g
     * @return
     */
    private Graph getMst(Graph g){
        Graph inter = new Graph(g.getV());
        Graph inter2 = new Graph(g.getV());
        /*Apply two septs of boruvka*/
        BoruvkaMST.applyBoruvkaStep(g, inter);
        inter.updateV();
        if(inter.getV() == 1)
            return inter;
        BoruvkaMST.applyBoruvkaStep(inter, inter2);
        BoruvkaMST.cleanGraph(inter2);
        inter2.updateV();
        if(inter2.getV() == 1)
            return inter2;
        /*get subgraph of mst*/
        Graph subGraph = new Graph(mst.getV());
        for(Edge e : mst.getAllEdges()){
            if(Randomizer.takeItOrNot())
                subGraph.addEdge(e);
        }
        subGraph.updateV();
        return getMst(subGraph);
    }

    /**
     * Second recursion F2
     * @param g
     * @return
     */
    private Graph getF2(Graph g){
        Graph inter = new Graph(g.getV());
        Graph inter2 = new Graph(g.getV());
        Graph g2 = new Graph(g.getV());
        /*Apply two septs of boruvka*/
        BoruvkaMST.applyBoruvkaStep(g, inter);
        inter.updateV();
        if(inter.getV() == 1)
            return inter;
        BoruvkaMST.applyBoruvkaStep(inter, inter2);
        BoruvkaMST.cleanGraph(inter2);
        inter2.updateV();
        if(inter2.getV() == 1)
            return inter2;
        /*get mst of a subgraph chosen randomly*/
        mst = getMst(inter2);
        int maxWeight = mst.getMaxWeight();
        for(Edge e : g.getAllEdges()){
            if(e.getWeight() < maxWeight)
                g2.addEdge(e);
        }
        return g2;
    }

    public static void main(String[] args) throws CloneNotSupportedException {
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
        RandomizedAlgo b = new RandomizedAlgo(bis);
       // processRandomizedAlgo(bis);
       // Graph clone = bis.clone();
       // System.out.println(bis);
       // System.out.println(clone);
       // System.out.println(processRandomizedAlgo(bis).toStringInit());
        //processRandomizedAlgo(bis);
       // Graph mst =  b.getMst();
        for(Edge e : processRandomizedAlgo(bis).getAllEdges()){
            System.out.println(e.toStringInit());
        }
        //System.out.println(b.getWeightMst());*/
    }

}
