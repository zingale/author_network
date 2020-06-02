First, create a token to access the ADS api

http://adsabs.github.io/help/api/

Copy this token into a file called .ads/dev_key

A sample driver looks like:

import author_network as an

names = ["Hix, W",
         "Calder, A",
         "Dubey, A",
         "Fuller, G",
         "Kasen, D",
         "Mezzacappa, A",
         "Roberts, L",
         "Steiner, A",
         "Burrows, A",
         "Couch, S",
         "Fryer, C",
         "Nonaka, A",
         "Messer, O",
         "Reddy, S",
         "Surman, R",
         "Zingale, M"]
         
an.create_network(names, year=2015)
