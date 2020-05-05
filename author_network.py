#!/usr/bin/env python3

import ads

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


names = ["Fryer, C",
         "Hartmann, D",
         "Kouveliotou, C",
         "White, N",
         "Zingale, M"]


team = {}

for nm in names:
    print(f"Team member {nm}")
    team[nm] = TeamMember(nm)
    for cauth in names:
        if nm == cauth:
            continue
        team[nm].add_coauthor(cauth)
    team[nm].show_connections()


me = AuthorPapers("Zingale, M")
#print(me.get_coauthors())
print(me.get_num_connections("Almgren"))

