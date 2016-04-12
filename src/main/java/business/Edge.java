package business;

/**
 * Created by lucas on 12/04/16.
 */
public class Edge implements Comparable<Edge> {

    //VW sont des ints qui permettent de representer les sommets
    private int v;
    private int w;
    //Poids de l'arete
    private int weight;

    public Edge(int v, int w, int weight) {
        this.v = v;
        this.w = w;
        this.weight = weight;
    }

    public int getWeight() {
        return weight;
    }

    /**
     * Retourne un des sommets de l'arete. Arbitrairement j'ai choisi v
     * @return
     */
    public int either() {
        return v;
    }

    /**
     * Retourne l'autre sommet de l'arete par rapport a celui passé en paramètre
     * @return -1 => erreur
     */
    public int other(int endPoint) {
        if (endPoint == v)
            return w;
        else if (endPoint == w)
            return v;
        else
            return -1;
    }

    public boolean sameEdge(Edge edge){
        if(v == edge.either() && w == edge.other(edge.either()))
            return true;
        else if (w == edge.either() && v == edge.other(edge.either()))
            return true;
        return false;
    }

    @Override
    public int compareTo(Edge o) {
        if (this.weight < o.getWeight())
            return -1;
        else if (this.weight > o.getWeight())
            return 1;
        else
            return  0;
    }

    @Override
    public String toString() {
        return "{" +
                "v=" + v +
                ", w=" + w +
                ", weight=" + weight +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Edge edge = (Edge) o;

        if (v != edge.v) return false;
        if (w != edge.w) return false;
        return weight == edge.weight;

    }

    public static void main(String[] args) {
        Edge e1 = new Edge(3,4,10);
        Edge e2 = new Edge(3,4,7);
        System.out.println("true = " + e1.equals(e2));
        Edge e3 = new Edge(4,3,12);
        System.out.println("true = " + e1.equals(e3));
        Edge e4 = new Edge(4,8,10);
        System.out.println("false = " + e1.equals(e4));
    }
}
