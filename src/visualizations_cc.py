import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
    weights = []
    max_acc = 0
    max_w = 0
    avg_cc = find_avg_cc(G)

    for w in np.arange(weight_range_lower, weight_range_higher, weight_interval):
        weights.append(w)
        com = dcn.findCommunities(G, i, thre=w * avg_cc)

        if len(com) > 100:
            print("predicted community is larger than actual:", (len(com) - 100))
            print("\tWeight:", w)

        acc = find_acc(com, i, i + 100)
        if acc > max_acc:
            max_acc = acc
            max_w = w

        accs.append(acc)

    print()
    print("Max accuracy:", round(max_acc, 4), "\n\tWeight:", max_w, "\n\tThreshold:", round(max_w * avg_cc, 4))
    return pd.DataFrame({"weight": weights, "accuracy": accs})


def thred_acc_plot(data):
    sns.lineplot(data=data, x="weight", y="accuracy")
    plt.title("Thresholds vs. Accuracy")
    plt.show()
    plt.close()


def accReal(pred_com, actual_com):
    correct = 0
    for x in pred_com:
        if x in actual_com:
            correct += 1
    return correct / len(actual_com)
