package misc;

import graph_structure.Node;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.Queue;

public class Helper {

	public static void printQ(Queue<Node> Q) {
		Iterator<Node> iterate = Q.iterator();
		StringBuffer result = new StringBuffer();
		while (iterate.hasNext()) {
			result.append(iterate.next().getData() + "-> ");
		}
		System.out.println(result);
	}
	
	public static void printList(ArrayList<Node> A) {
		StringBuffer result = new StringBuffer();
		for (Node N: A) {
			result.append(N.getData() + ", ");
		}
		System.out.println(result);
	}
	
}
