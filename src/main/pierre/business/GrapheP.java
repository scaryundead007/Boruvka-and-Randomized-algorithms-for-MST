package business;

import java.util.ArrayList;

/**
 * Created by Simon on 13/04/16.
 */
public class GrapheP {

    private ArrayList<VertexP> vertexs;
    private ArrayList<EdgeP> edges;

    public GrapheP(ArrayList<VertexP> v, ArrayList<EdgeP> e) {
        this.vertexs = v;
        this.edges = e;
    }


    public ArrayList<VertexP> getVertexs() {
        return vertexs;
    }

    public ArrayList<EdgeP> getEdges() {
        return edges;
    }

    public void setVertexs(ArrayList<VertexP> vertexs) {
        this.vertexs = vertexs;
    }

    public void setEdges(ArrayList<EdgeP> edges) {
        this.edges = edges;
    }
}
