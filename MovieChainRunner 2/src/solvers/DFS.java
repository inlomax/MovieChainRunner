package solvers;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Set;

import misc.Helper;
import graph_structure.Graph;
import graph_structure.Node;

public class DFS {
	private Graph G;
	
	public DFS(Graph G) {
		this.G = G;
	}
	
	public Queue<Node> findLongestChain() {
		int max_size = -1;
		Queue<Node> max_chain = null;
		Set<Node> nodes = G.getNodes();
		Iterator<Node> iter = nodes.iterator();
		for (int i = 0; i <10; i++) {
			Queue<Node> cur_chain = findChain(iter.next());
			if (cur_chain.size() > max_size) {
				max_size = cur_chain.size();
				max_chain = cur_chain;
			}
		}
		return max_chain;
	}
	
	public Queue<Node> findChain(Node N) {
		System.out.println("Entering node: " + N.getData());
		HashSet<Node> seen = new HashSet<Node>();
		seen.add(N);
		Queue<Node> chain = new LinkedList<Node>();
		chain.add(N);
		Queue<Node> result = findChainHelper(N, seen, chain);
		Helper.printQ(result);
		System.out.println();
		return result;
	}
	
	public Queue<Node> findChainHelper(Node N, HashSet<Node> seen, Queue<Node> chain) {
		
		ArrayList<Node> neighbors = G.getNeighbors(N);
		if ((chain.size() == 1) &&neighbors.isEmpty()){
			System.out.println(N.getData() + " has no neighbors");
			return chain;
		}
		else if (chain.size() == 1){
			System.out.println(N.getData() + " neighbors: ");
			Helper.printList(neighbors);
		}
		
		boolean contains_unseen_neighbor = false;
		int longest_child_chain_length = -1;
		Queue<Node> longest_chain = null;
		for (Node neighbor: neighbors) {
			if (!seen.contains(neighbor)) {
				contains_unseen_neighbor = true;
				HashSet<Node> seen_copy = makeDeepCopy(seen);
				Queue<Node> chain_copy = makeDeepCopy(chain);
				seen_copy.add(neighbor);
				chain_copy.add(neighbor);
				Queue<Node> cur_chain = findChainHelper(neighbor, seen_copy, chain_copy);
				if (cur_chain.size() > longest_child_chain_length) {
					longest_child_chain_length = cur_chain.size();
					longest_chain = cur_chain;
				}
			}
		}
		if (!contains_unseen_neighbor) return chain;
		else return longest_chain;
	}
	
	public HashSet<Node> makeDeepCopy(HashSet<Node> old_set) {
		HashSet<Node> copy = new HashSet<Node>();
		
		Iterator<Node> iterate = old_set.iterator();
		while (iterate.hasNext()) {
			copy.add(iterate.next());
		}
		return copy;
	}
	
	public Queue<Node> makeDeepCopy(Queue<Node> old_q) {
		Queue<Node> copy = new LinkedList<Node>();
		
		Iterator<Node> iterate = old_q.iterator();
		while (iterate.hasNext()) {
			copy.add(iterate.next());
		}
		return copy;
	}

}
