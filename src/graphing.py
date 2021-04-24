from __future__ import annotations
import os
from collections import defaultdict
import itertools
import networkx as nx
import pandas as pd

def character_graph(name_lists: list[str]) -> nx.Graph:
    """
    Weight is +1 to edge between two characters if they appear in same name list
    """
    edges = defaultdict(lambda: 0)
    for L in name_lists:
        for edge in itertools.combinations(L, r=2): # All pairs of characters
            # Make sure that there is not a difference between (Ned, Sansa) and (Sansa, Ned)
            edge = tuple(sorted(edge))
            edges[edge] += 1
    max_w = max(edges.values())
    G = nx.Graph()
    G.add_weighted_edges_from(((*e, w/max_w) for e, w in edges.items()), weight="weight")
    return G

if __name__ == '__main__':
    # dataset = "asoiaf_data_cleaned"
    dataset = "book"

    datapath = "data"
    localdatapath = "local_data"

    df = pd.read_csv(os.path.join(localdatapath, f"{dataset}.csv"), header=0, index_col = 0)
    df["names"] = df.apply(lambda r: eval(r["names"]), axis=1)

    G = character_graph(df["names"])
    print("Saving graph to file ...")
    nx.write_gpickle(G, os.path.join(datapath, f"{dataset}.nxgraph"))
