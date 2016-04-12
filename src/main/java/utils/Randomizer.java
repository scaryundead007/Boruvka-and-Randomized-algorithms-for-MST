package utils;

import java.util.Random;

/**
 * Created by lucas on 12/04/16.
 */
public class Randomizer {
    public static Random rand = new Random();

    public final static int K_WEIGHT_MAX = 50;
    public final static int K_WEIGHT_MIN = 0;

    public static int getRandom(int beginning, int end){
        return beginning + rand.nextInt(end - beginning);
    }

    public static int getWeight(){
        return K_WEIGHT_MIN + rand.nextInt(K_WEIGHT_MAX - K_WEIGHT_MIN);
    }

    public static int[] getDiffRandoms(int beginning, int end){
        if(end - beginning  <= 1)
            return null;
        int nb1 = 0;
        int nb2 = 0;
        while(nb1 == nb2) {
            nb1 = getRandom(beginning, end);
            nb2 = getRandom(beginning, end);
        }
        return new int[]{nb1, nb2};
    }

    public static void main(String[] args) {
        System.out.println(getWeight());
    }
}
