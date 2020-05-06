#!/usr/bin/env python3

import ads
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class AuthorPapers:

    def __init__(self, name):
        p = list(ads.SearchQuery(author=name,
                                 max_pages=10,
                                 fl=["id", "bibcode", "citation_count",
                                     "author", "year", "property"]))

        self.mypapers = p
        self.num = len(self.mypapers)

    def get_coauthors(self):
        """get the list of unique coauthor lastnames"""
        a = []
        for p in self.mypapers:
            a += [q.split()[0] for q in p.author]
        return sorted(set(a))

    def get_num_connections(self, coauthor, year=0):
        """return the number of papers shared with coauthor"""
        colast = coauthor.split()[0].replace(",", "")
        n = 0
        for p in self.mypapers:
            for auth in p.author:
                authlast = auth.split()[0].replace(",", "")
                if colast.lower() == authlast.lower():
                    n += 1
        return n


class TeamMember:

    def __init__(self, name):

        self.papers = AuthorPapers(name)

        self.coauthors = {}

    def add_coauthor(self, coauthor):
        self.coauthors[coauthor] = self.papers.get_num_connections(coauthor)

    def show_connections(self):
        for c in self.coauthors:
            print(c, self.coauthors[c])


def create_network(names, layout="spring", outfile="authors.png"):

    team = {}

    for nm in names:
        print(f"Team member {nm}")
        team[nm] = TeamMember(nm)
        for cauth in names:
            if nm == cauth:
                continue
            team[nm].add_coauthor(cauth)
        team[nm].show_connections()

    G = nx.Graph()

    for nm in names:
        for cauth in team[nm].coauthors:
            num = team[nm].coauthors[cauth]
            if num > 0:
                G.add_edge(nm, cauth, weight=num)

    if layout == "spring":
        pos = nx.spring_layout(G)
    elif layout == "circle":
        pos = nx.circular_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=400)

    edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())
    weights = np.clip(np.array(weights), 1, 10)

    colors = np.arange(len(weights)) + 1
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=weights,
                           edge_color=colors)

    # raise the text positions
    for p in pos:
        pos[p][1] += 0.1
    nx.draw_networkx_labels(G, pos, zorder=100, font_size=10)


    plt.axis("off")
    plt.margins(0.1)
    #plt.tight_layout()
    plt.savefig(outfile)


if __name__ == "__main__":

    names = ["Fryer, C",
             "Hartmann, D",
             "Kouveliotou, C",
             "White, N",
             "Zingale, M"]

    create_network(names)
