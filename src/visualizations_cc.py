import networkx as nx
import numpy as np
import pandas as pd

import src.DFS_common_neighbor as dcn


def find_acc(community, community_range_lower, community_range_higher):
    correct_preds = 0
    for x in community:
        if x in range(community_range_lower, community_range_higher):
            correct_preds += 1
    return correct_preds / max(len(community), community_range_higher - community_range_lower)


def find_avg_cc(G):
    avg = 0
    for i in G.nodes:
        for j in G.nodes:
            if i == j:
                continue

            avg += len(list(nx.common_neighbors(G, i, j)))

    return avg / G.order()


def tuning_thred(weight_range_lower, weight_range_higher, weight_interval, G, i):
    accs = []
    threds = []
    avg_cc = find_avg_cc(G)

    for w in np.arange(weight_range_lower, weight_range_higher, weight_interval):
        th = w * avg_cc
        threds.append(th)
        com = dcn.findCommunities(G, i, thre=w * avg_cc)
        acc = find_acc(com, i, i + 100)
        accs.append(acc)

    da = pd.DataFrame({"threshold": threds, "accuracy": accs})
    return da
