package misc;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import graph_structure.Graph;
import graph_structure.Node;

public class GraphConstructor {
	private static final boolean IS_TESTING = true;
	
	public static Graph buildGraph() {
			ArrayList<Node> nodes;
			try {
				nodes = readFromFile();
				return buildGraphFromNodes(nodes);
			} catch (IOException e) {
				e.printStackTrace();
			}
			return null;
	}
	
	public static Graph buildGraphFromNodes(ArrayList<Node> nodes) {
		HashMap<Node, ArrayList<Node>> result = new HashMap<Node, ArrayList<Node>>();
		ArrayList<Node> cur_neighbors;
		int counter = 0;
		for (Node source: nodes) {
			if (counter % 500 == 0) {
				System.out.println("GRAPH CONSTRUCTING..." + counter);
			}
			cur_neighbors = new ArrayList<Node>();
			for (Node dest: nodes) {
				if (source == dest) continue;
				if (doesOverlap(source.getData(), dest.getData())) {
					cur_neighbors.add(dest);
				}
			}
			result.put(source, cur_neighbors);
			counter += 1;
		}
		System.out.println("GRAPH FULLY CONSTRUCTED");
		return new Graph(result);
	}
	
	public static ArrayList<Node> readFromFile() throws IOException {
		String default_path = System.getProperty("user.dir");
		String file_path = "/Users/tanayvarma/Desktop/Movie_list.txt";
		//String file_path = default_path + "\\src\\test_movies_1.txt";
		FileReader fr = new FileReader(file_path);
        BufferedReader txt = new BufferedReader(fr);
        
        ArrayList<Node> nodes = new ArrayList<Node>();
        String line;
        while ((line = txt.readLine()) != null) {
            Node new_node = new Node(line);
            nodes.add(new_node);
        }
        txt.close();
        fr.close();
        return nodes;
	}
	
	public static boolean doesOverlap(String f, String s) {
		if(f.equals(s)) return false;
	       
		String[] f_arr = f.split(" ");
		int l1 = f_arr.length;
		String[] s_arr = s.split(" ");
		int l2 = s_arr.length;
		
		String str_f = "";
		String str_s = "";
		   
		for(int i = 0; i < Math.min(l1,l2); i++) {
			str_f = f_arr[l1-1-i] + str_f;
			str_s = str_s + s_arr[i];    
			if (str_f.equals(str_s)) {
				return true;
			}
			str_f = " "+str_f;
			str_s = str_s+" ";
		}
		return false;
	}
	
	public static void testPrint(String S) {
		if (IS_TESTING) {
			System.out.println(S);
		}
	}
}
