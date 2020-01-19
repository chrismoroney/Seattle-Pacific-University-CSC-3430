/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package csc3430p1;
import java.io.*;

/**
 *
 * @author chrismoroney
 */
public class CSC3430P1 {

    /**
     * @param args the command line arguments
     * @throws java.io.IOException
     * @throws java.lang.InterruptedException
     */
    public static void main(String[] args) throws IOException, InterruptedException {
        try (PrintWriter out = new PrintWriter("CSC3430P1.csv")) {
            // set base to given value
            double base = 3.14159265359;
            // this is pretty much the limit that my macbook pro and netbeans can take on
            // before getting a stack overflow exception, was a number that was 
            // tested until the overflow caused the computer to crash
            int limit = 39681;
            // This is the header section of my csv file, just to give labels 
            // to my csv file, using a StringBuilder
            StringBuilder header = new StringBuilder("");
            header.append("n");
            header.append(", ");
            header.append("iterator-time");
            header.append(", ");
            header.append("recursive-time");
            header.append("\n");
            // write this into my PrintWriter function
            out.write(header.toString());
            // in this, we are accounting for memory, so we delete (not as important
            // as the data.delete below)
            header.delete(0, header.length());
            
            // Now we are going to make the data in this section with StringBuilder
            StringBuilder data = new StringBuilder("");
            // make a for loop from 1 until we finish iterating with the limit 
            for (int i = 0; i <= limit; i++){
                // start nanosecond timer, create two instances of it
                // first instance stops when program reaches up to the point of function
                long start = System.nanoTime();
                // complete the function, we call on a double because we just want
                // to be able to return a value to see if function works
                double returnVal = iterativePower(base, i);
                // second nanotimer, stops when program finishes the power function
                long end = System.nanoTime();
                // take the second timer and subtract by first, and thats how much
                // time the program took
                long firstTime = (end - start);
                
                // same thing as above, but we are using with recursive function now
                long start2 = System.nanoTime();
                double returnVal2 = recursivePower(base, i);
                long end2 = System.nanoTime();
                long secondTime = (end2 - start2);
                
                // load the times into our PrintWriter csv file
                // i represents our n exponent
                data.append(i);
                data.append(",");
                // firstTime represents the iterative time
                data.append(firstTime);
                data.append(",");
                // secondTime represents the recursive time
                data.append(secondTime);
                data.append("\n");
                
                // convert the data into a string so that PrintWriter can print
                String printVal = data.toString();
                // print into the file
                out.print(printVal);
                // we have to delete what we put into our StringBuilder. If we
                // keep what we have, we are going to be reprinting all of the previous
                // values we have, when all we want is to print the values
                // of this certain time in the for loop, prevents repetition and 
                // acounts for memory when we are done.
                data.delete(0, data.length());
            }
        }
    }
    // provided iterative Power function, return val only used to catch the 
    // function in main
    public static double iterativePower(double base, int n){
        double returnVal = 1.0;
        if (n < 0){
            return 1.0 / iterativePower(base, -n);
        } else {
            for (int i = 0; i < n; i++){
                returnVal *= base;
            }
        }
        return returnVal;
    }
    // provided recursive Power function, return val only used to catch the 
    // function in main
    public static double recursivePower(double base, int n){
        if (n < 0){
            return 1.0/recursivePower(base, -n);
        } else if (n == 0){
            return 1.0;
        } else {
            return base * recursivePower(base, n - 1);
        }
    }
}
