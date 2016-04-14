package business;

import java.util.ArrayList;

/**
 * Created by Simon on 13/04/16.
 */
public class VertexP {

    private String name;
    private ArrayList<EdgeP> edges;

    public VertexP(String n, ArrayList<EdgeP> l) {
        this.name = n;
        this.edges = l;
    }


    public String getName() {
        return name;
    }

    public ArrayList<EdgeP> getEdges() {
        return edges;
    }


    public void setName(String name) {
        this.name = name;
    }

    public void setEdges(ArrayList<EdgeP> edges) {
        this.edges = edges;
    }
}
