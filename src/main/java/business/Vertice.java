package business;

/**
 * Created by lucas on 13/04/16.
 */
public class Vertice {

    private int nb;

    public Vertice(int nb) {
        this.nb = nb;
    }

    public int getNb() {
        return nb;
    }

    @Override
    public String toString() {
        return Integer.toString(nb);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Vertice vertice = (Vertice) o;

        return nb == vertice.nb;

    }

    @Override
    public int hashCode() {
        return nb;
    }
}
