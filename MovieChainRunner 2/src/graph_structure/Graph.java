package graph_structure;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;

public class Graph {
	private HashMap<Node, ArrayList<Node>> adj_list;
	
	public Graph(HashMap<Node, ArrayList<Node>> adj_list) {
		this.adj_list = adj_list;
	}
	
	public ArrayList<Node> getNeighbors(Node N) {
		return adj_list.get(N);
	}
	
	public void printGraph() {
		Set<Node> nodes = adj_list.keySet();
		StringBuffer cur_string;
		for (Node N: nodes) {
			cur_string = new StringBuffer();
			cur_string.append(N.getData() + ": ");
			ArrayList<Node> neighbors = adj_list.get(N);
			for (Node neighbor: neighbors) {
				cur_string.append(neighbor.getData() + ", ");
			}
			System.out.println(cur_string);
		}
	}
	
	public Set<Node> getNodes() {
		return adj_list.keySet();
	}
}
