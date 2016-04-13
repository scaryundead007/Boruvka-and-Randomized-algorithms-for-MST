import business.EdgeP;
import business.GrapheP;
import business.VertexP;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

/**
 * Created by Simon on 13/04/16.
 */

public class Boruvka {
    GrapheP graph;
    Set<EdgeP> T;
    Set<EdgeP> newestEdges;
    Set<VertexP> Comp;

    public Boruvka(GrapheP g) {
        this.graph = g;
        this.T = new HashSet<EdgeP>();
        this.T = new HashSet<EdgeP>();
        this.Comp = fillComp();
    }

    public Set<VertexP> fillComp() {
        ArrayList<VertexP> vertexs = graph.getVertexs();
        int s = vertexs.size();
        Set<VertexP> res = new HashSet<>();
        for (int i = 0; i < s; i++) {
            res.add(vertexs.get(i));
        }
        return res;
    }

    public EdgeP FindLowestEdge(VertexP v) {
        ArrayList<EdgeP> edges = v.getEdges();
        int s = edges.size();
        int weight = 0;
        EdgeP res = null;
        for (int i = 0; i < s; i++) {
            int w = edges.get(i).getWeight();
            if (w < weight) {
                weight = w;
                res =  edges.get(i);
            }
        }
        return res;
    }

    public void contract() {
        for (EdgeP e : newestEdges) {
            e.getFoo().getName()
        }
    }

    public Set<EdgeP> process() {
        while (Comp.size() != 1) {
            for (VertexP v : Comp) {
                EdgeP e = FindLowestEdge(v);
                T.add(e); newestEdges.add(e);
            }

        }
        return T;
    }

    public static void main(String[] args) {
        System.out.println("il va faire tout noir");
    }

}
