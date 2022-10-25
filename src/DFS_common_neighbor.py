import networkx as nx


def numCommonNeighbors(G, i, j):
    # use networkx methods to find the number of common neighbors
    return len(list(nx.common_neighbors(G, i, j)))


def dfs_cn(G, i, visited, curCommunity, thre):
    # As i NOTE: Since I observe this
    # implementation seems works not very well, I think we can only compare the new node j with root i
    # In other words, compute the number of common neighbor between root and node j
    if i in visited:
        return

    visited.add(i)
    neighbors = list(nx.neighbors(G, i))

    for j in neighbors:  # search for all neighbors
        num_cn = numCommonNeighbors(G, i, j)

        if num_cn >= thre:  # if the number of common neighbors is greater than the threshold
            curCommunity.add(j)  # we think the neighbor should also be in the same community
        else:
            visited.add(j)

        dfs_cn(G, j, visited, curCommunity, thre)


def findCommunities(G, i, thre=5):
    com = set()
    com.add(i)
    visited = set()
    # use DFS to search the vertices which is also within the same community. As i NOTE: Since I observe this
    # implementation seems works not very well, I think we can only compare the new node j with root i

    dfs_cn(G, i, visited, com, thre)

    return com
