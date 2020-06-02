#!/usr/bin/env python3

import ads
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def clean_author(name):
    """ make the author name of the form 'last, x', where 'x' is the first initial"""
    parts = name.split(",")
    lastname = parts[0].strip().lower()
    try:
        fi = parts[1].strip().lower()[0]
        return "{}, {}".format(lastname, fi)
    except IndexError:
        return lastname

class AuthorPapers:

    def __init__(self, name, year=None):
        p = list(ads.SearchQuery(author=name,
                                 max_pages=10,
                                 fl=["id", "bibcode", "citation_count",
                                     "author", "year", "property"]))

        # filter by year, if desired
        if year is None:
            self.mypapers = p
        else:
            pyr = [q for q in p if int(q.year) >= year]
            self.mypapers = pyr

        self.num = len(self.mypapers)

    def get_coauthors(self):
        """get the list of unique coauthor lastnames"""
        a = []
        for p in self.mypapers:
            a += [clean_author(q) for q in p.author]
        return sorted(set(a))

    def get_num_connections(self, coauthor, year=0):
        """return the number of papers shared with coauthor"""
        colast = clean_author(coauthor)
        n = 0
        for p in self.mypapers:
            for auth in p.author:
                authlast = clean_author(auth)
                if colast == authlast:
                    n += 1
        return n


class TeamMember:

    def __init__(self, name, year=None):

        self.papers = AuthorPapers(name, year=year)

        self.coauthors = {}

    def add_coauthor(self, coauthor):
        self.coauthors[coauthor] = self.papers.get_num_connections(coauthor)

    def show_connections(self):
        for c in self.coauthors:
            print(c, self.coauthors[c])
        print()

def create_network(names, year=None,
                   layout="spring", outfile="authors.png"):

    team = {}

    for nm in names:
        print(f"Team member {nm}")
        team[nm] = TeamMember(nm, year=year)
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


