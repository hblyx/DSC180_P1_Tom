import networkx as nx

from src.data import create_test_graph as test
from src.features import read_graph as read
from src.models import common_neighbor_community as cnc



G, actual_com = test.createTestGraph()
test.createTestData(G, actual_com)

G = read.createGraph("test/testdata/test_graph.txt")
actual_com = read.createActualCommunity("test/testdata/test_community.txt")

CNC = cnc.CommonNeighborCommunity(G, actual_com)
CNC.findAllCommunities(thres=0.1, weighted=True)
print("Test Success:", CNC.getAvgAccuracy() == 1.0)