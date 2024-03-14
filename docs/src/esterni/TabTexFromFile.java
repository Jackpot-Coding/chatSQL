package esterni;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class TabTexFromFile {

    static int countLines(Scanner sc) {
        int count = 0;
        while (sc.hasNextLine()) {
            count++;
            sc.nextLine();
        }
        return count;
    }

    static String rowToLatex(String row[]) {
        String s = "          " ;
        for(int i = 0; i < row.length-1; i++) {
            s =  s + row[i] + " & ";
        }
        s = s + row[row.length-1] + " \\\\ \\hline";
        return s;
    }

    static String getRow(String row, boolean firstRow) {
        String s[] = row.split("\t");
        if(firstRow) {
            for(int i = 0; i < s.length; i++) s[i] = "\\textbf{" + s[i] + "}";
        }
        return rowToLatex(s);
    }

    static void printTab(Scanner sc, int lines) {
        int word = 0;
        String rows[] = new String[lines];
        while (sc.hasNextLine()) {
            rows[word] = sc.nextLine();
            word++;
        }
        for(int i = 0; i < lines; i++) {
            boolean firstRow = false;
            if(i == 0) firstRow = true; 
            System.out.println(getRow(rows[i], firstRow));
        }
    }

    static void printFirst() {
        System.out.println("    \\begin{table}[H]\r\n" + //
                        "      \\centering\r\n" + //
                        "      \\rowcolors{2}{black!15}{}\r\n" + //
                        "      \\resizebox{\\linewidth}{!}{\r\n" + //
                        "        \\begin{tabular}{|c|c|c|c|c|c|c|c|}\r\n" + //
                        "          \\hline\r\n" + //
                        "          \\rowcolor{teal!50}");
    }

    static void printLast() {
        System.out.println("        \\end{tabular}\r\n" + //
                        "      }\r\n" + //
                        "      \\caption{}\r\n" + //
                        "    \\end{table}");
    }

    public static void main(String args[]) {
        File file = new File(
            "docs\\src\\esterni\\tab.txt");
        try {

            printFirst();
            printTab(new Scanner(file), countLines(new Scanner(file)));
            printLast();
            
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
}