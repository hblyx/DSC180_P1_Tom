import networkx as nx



class CommonNeighborCommunity:
    def __init__(self, G: nx.Graph, thres: float, actual_com: dict = None, weighted: bool = False) -> None:
        """
        Create an object to find communities based on number of common neighbors
        
        
        Parameters
        ----------
        G : networkx.Graph
            An undirected graph which used to detect communities
        thres : float
            Threshold to determine whether two nodes are within the same community
        actual_com : dict = None
            Dictionary indicating the actual community, ground truth, of the graph
            If None, there is no ground truth for community
        weighted : bool = False
            Wether using weighted threshold, use weighted * total_degree to determine the threshold
        """
        
        self.G = G
        self.thres = thres
        self.weighted = weighted
        
        if actual_com is not None:
            self.setActualCommunities(actual_com)

        self.resetPredCommunities()
        self.communityCount = 0
        
        
        
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
    
    
    
    def exceedThreshold(self, num_common_neighbors, i, j) -> bool:
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
        
        if self.weighted:
            # sum of two nodes degree = sum of degree - 1 
            # where the 1 is the duplicate edge from i to j
            return num_common_neighbors >= self.thres * (self.G.degree[i] + self.G.degree[j] - 1)
        else:
            return num_common_neighbors >= self.thres
    
    
    
    def DFS_common_neighbors(self, i, visited: set, cur_com: set) -> None:
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
        """
        
        if i in visited: # if visited 
            return
        
        visited.add(i)
        
        for j in nx.neighbors(self.G, i):
            if not self.G.nodes[j]["has_pred"]:
                num_common_neighbors = num_common_neighbors(i, j)
                
                if self.exceedThreshold(num_common_neighbors, i, j):
                    cur_com.add(j)
                #else:
                #    visited.add(j)
            
            self.DFS_common_neighbors(j, visited, cur_com)
            
            
            
    def findCommunity(self, i) -> None:
        """
        Use DFS and number of common neighbors to find community of a node i
        
        
        Parameters
        ----------
        i : graph node
            The node used to find community
        """
        
        community = set()
        community.add(i)
        visited = set()
        
        self.DFS_common_neighbors(i, visited, community)
        
        self.assignCommunity(community)
        
        
    
    def assignCommunity(self, community: set) -> None:
        """
        Assign found predicted community to graph within the nodes' attributes
        
        
        Parameters
        ----------
        community : set
            Found predicted community to assign
        """
        
        for i in community:
            self.G.nodes[i]["pred_com"] = self.communityCount
            self.G.nodes[i]["has_pred"] = True
        
        self.communityCount += 1



    def setActualCommunities(self, actual_com: dict) -> None:
        """
        Take the community dictionary and embed the actual community information into the nodes' attributes
        
        
        Parameters
        ----------
        actual_com : dict
            Actual community/ ground truth communities dictionary
        """
        
        nx.set_node_attributes(self.G, actual_com, name="actual_com")
        
        

    def resetPredCommunities(self) -> None:
        """
        Resset the communities prediction on the graph
        """
        
        nx.set_node_attributes(self.G, None, name="pred_com")
        nx.set_node_attributes(self.G, False, name="has_pred")
        
        
        
    def getGraph(self) -> nx.Graph:
        """
        Get the graph with information including communities prediction and ground truth communities
        """
        
        return self.G
    
    