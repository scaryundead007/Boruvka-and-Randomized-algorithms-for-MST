package Kruskal;

import java.util.ArrayList;

public class ListeChainee {
    int num;
    ListeChainee suivant;
    ArrayList<Integer> liste = new ArrayList<Integer>();

    public ListeChainee(int num) {
        this.num = num;
    }

    public void addAdjacent(int num) {
        liste.add(num);
    }
}