package business;

/**
 * Created by lucas on 12/04/16.
 */
public class Edge implements Comparable<Edge> {

    //VW sont des ints qui permettent de representer les sommets
    private int v;
    private int w;
    //Poids de l'arete
    private double weight;

    public Edge(int v, int w, double weight) {
        this.v = v;
        this.w = w;
        this.weight = weight;
    }

    public double getWeight() {
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
        return "Edge{" +
                "v=" + v +
                ", w=" + w +
                ", weight=" + weight +
                '}';
    }
}
