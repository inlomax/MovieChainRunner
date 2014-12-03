package misc;

import java.util.Queue;

import solvers.DFS;
import graph_structure.Graph;
import graph_structure.Node;

public class Main {

	public static void main(String[] args) {
		Graph G = GraphConstructor.buildGraph();
		
		DFS solver = new DFS(G);
		Queue<Node> answer = solver.findLongestChain();
		
		System.out.println("OVERALL RESULT: ");
		Helper.printQ(answer);
	}

}
