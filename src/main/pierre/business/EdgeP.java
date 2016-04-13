package business;

/**
 * Created by Simon on 13/04/16.
 */

public class EdgeP {

    private VertexP foo;
    private VertexP bar;
    private int weight;

    public EdgeP(VertexP s, VertexP e, int w) {
        this.foo = s;
        this.bar = e;
        this.weight = w;
    }


    public VertexP getFoo() {
        return foo;
    }

    public VertexP getBar() {
        return bar;
    }

    public int getWeight() {
        return weight;
    }

    public void setFoo(VertexP start) {
        this.foo = start;
    }

    public void setBar(VertexP end) {
        this.bar = end;
    }

    public void setWeight(int weight) {
        this.weight = weight;
    }
}
