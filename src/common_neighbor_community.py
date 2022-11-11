import networkx as nx
import pandas as pd



class CommonNeighborCommunity:
    def __init__(self, G: nx.Graph, actual_com: dict = None) -> None:
        """
        Create an object to find communities based on number of common neighbors
        
        
        Parameters
        ----------
        G : networkx.Graph
            An undirected graph which used to detect communities
        actual_com : dict = None
            Dictionary indicating the actual community, ground truth, of the graph
            If None, there is no ground truth for community
        """
        
        self.G = G
        
        if actual_com is not None:
            self.setActualCommunities(actual_com)

        self.resetPredCommunities()
        self.num_pred_com = 0
        self.num_preds = 0
        
        
        
    def numCommonNeighbors(self, i, j) -> int:
        """
        Use networkx methods to find the number of common neighbors but this is only for un directed graphs
        
        
        Parameters
        ----------
        i : graph node
            A node in the graph
        j : graph node
            Another node in the graph
            
        Return
        ------
        output : int
            number of common neighbors between two nodes
        """
        
        return len(list(nx.common_neighbors(self.G, i, j)))
    
    
    
    def exceedThreshold(self, num_common_neighbors, i, j, thres, weighted: bool = False) -> bool:
        """
        Determine whether the pair of node are within a same community based on the threshold
        
        
        Parameters
        ----------
        num_common_neighbors: int
            number of common neighbors between these two nodes
        i : graph node
            A node in the graph
        j : graph node
            Another node in the graph
            
        Return
        ------
        output : bool
            whether the number of common neighbors exceed the threshold
        """
        
        if weighted:
            # sum of two nodes degree = sum of degree - 1 
            # where the 1 is the duplicate edge from i to j
            return num_common_neighbors >= thres * (self.G.degree[i] + self.G.degree[j] - 1)
        else:
            return num_common_neighbors >= thres
    
    
    
    def DFS_common_neighbors(self, i, visited: set, cur_com: set, thres: float, weighted: bool = False) -> None:
        """
        DFS to search whether nodes are within the community
        
        
        Parameters
        ----------
        i : graph node
            The node used to find community
        visited : set
            visited nodes for DFS
        cur_com : set
            the community has found so far
        thres : float
            Threshold to determine whether two nodes are within the same community
        weighted : bool = False
            Wether using weighted threshold, use weighted * total_degree to determine the threshold
        """
        
        if i in visited:
            return
        
        visited.add(i)
        
        for j in nx.neighbors(self.G, i):
            num_common_neighbors = self.numCommonNeighbors(i, j)
                
            if self.exceedThreshold(num_common_neighbors, i, j, thres, weighted):
                cur_com.add(j)
                self.DFS_common_neighbors(j, visited, cur_com, thres, weighted)
            
            
            
    def findCommunity(self, i, thres: float, weighted: bool = False) -> set:
        """
        Use DFS and number of common neighbors to find community of a node i
        
        
        Parameters
        ----------
        i : graph node
            The node used to find community
        thres : float
            Threshold to determine whether two nodes are within the same community
        weighted : bool = False
            Wether using weighted threshold, use weighted * total_degree to determine the threshold
            
        Return
        ------
        community: set
            The predicted community for node i
        """
        
        community = set()
        
        community.add(i)
        
        visited = set()
        
        self.DFS_common_neighbors(i, visited, community, thres, weighted=weighted)
        
        self.assignCommunity(community)
        
        return community
    
    
    
    def findAllCommunities(self, thres: float, weighted: bool = False) -> None:
        """
        Find all communities with DFS and number of common neighbors
        
        
        Parameters
        ----------
        thres : float
            Threshold to determine whether two nodes are within the same community
        weighted : bool = False
            Wether using weighted threshold, use weighted * total_degree to determine the threshold
        """
        
        # reset the predicitons
        self.resetPredCommunities()
        
        for i in self.G.nodes:
            if not self.G.nodes[i]["has_pred"]:
                self.findCommunity(i, thres, weighted=weighted)
                
        if self.num_preds == self.G.order():
            print("Made predictions for all nodes")
        else: 
            print(f"{self.num_preds}/{self.G.order()} nodes are made predictions")
        
        
    
    def assignCommunity(self, community: set) -> None:
        """
        Assign found predicted community to graph within the nodes' attributes
        
        
        Parameters
        ----------
        community : set
            Found predicted community to assign
        """
        
        for i in community:
            # if we find a community not only belongs to a single community
            #if self.G.nodes[i]["pred_com"] is None:
            #    self.G.nodes[i]["pred_com"] = set()
            #self.G.nodes[i]["pred_com"].add(self.num_pred_com)
            
            self.G.nodes[i]["pred_com"] = self.num_pred_com
            self.G.nodes[i]["has_pred"] = True
            self.num_preds += 1
        
        self.num_pred_com += 1



    def setActualCommunities(self, actual_com: dict) -> None:
        """
        Take the community dictionary and embed the actual community information into the nodes' attributes
        Since we need the community in order, we will ascendingly handle nodes, and community of lower nodes has lower community numbers
        
        
        Parameters
        ----------
        actual_com : dict
            Actual community/ ground truth communities dictionary
        """
        
        change_dict = {}
        com_count = 0
        
        for i in self.G.nodes:
            origin_com = actual_com[i]
            
            if origin_com not in change_dict: # new community
                change_dict[origin_com] = com_count
                com_count += 1
                
        for i in actual_com:
            origin_com = actual_com[i]
            
            actual_com[i] = change_dict[origin_com]
        
        nx.set_node_attributes(self.G, actual_com, name="actual_com")
        
        

    def resetPredCommunities(self) -> None:
        """
        Resset the communities prediction on the graph
        """
        
        nx.set_node_attributes(self.G, None, name="pred_com")
        nx.set_node_attributes(self.G, False, name="has_pred")
        self.num_preds = 0
        self.num_pred_com = 0
        
        print("Reset all predictions")
        
        
        
    def getGraph(self) -> nx.Graph:
        """
        Get the graph with information including communities prediction and ground truth communities
        
        Return
        ------
        self.G: networkx.Graph
            The graph with information including communities prediction and ground truth communities
        """
        
        return self.G
    
    def getResult(self) -> dict:
        """
        Use prediction made to output result of prediction and ground truth
            
        Return
        ------
        output: pandas.DataFrame
            A Pandas DataFrame which describes the result of predictions
        """
        
        pred_com = []
        actual_com = []
        nodes = []
        for i in self.G.nodes:
            pred_com.append(self.G.nodes[i]["pred_com"])
            actual_com.append(self.G.nodes[i]["actual_com"])
            nodes.append(i)
            
        return pd.DataFrame({"node": nodes, "pred_com": pred_com, "actual_com": actual_com}).set_index("node").sort_index()