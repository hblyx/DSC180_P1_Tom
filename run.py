# import src.create_test_graph as test
import src.read_graph as read
import src.common_neighbor_community as cnc
import networkx as nx

# G, actual_com = test.createTestGraph()
# test.createTestData(G, actual_com)

G = read.createGraph("test/testdata/test_graph.txt")
actual_com = read.createActualCommunity("test/testdata/test_community.txt")

CNC = cnc.CommonNeighborCommunity(G, actual_com)
CNC.findAllCommunities(thres=0.1, weighted=True)
print("Test Average Accuracy is:", CNC.getAvgAccuracy())