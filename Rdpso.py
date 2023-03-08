from igraph import *
import matplotlib.pyplot as plt
import math
import random
from IC_single import IC_single
from rdpso.problem import Problem
from rdpso.evolution import Evolution


edges = []
nodes = []
for line in open("twitter/facebook.edgelist"):
    u, v = line.split()
    edges.append((int(u), int(v)))
    nodes.append(int(u))
    nodes.append(int(v))
nodes = list(set(nodes))

g = Graph(edges)
weight = {}


for node in nodes:
    weight[node] = 1 / (len(g.neighbors(node, mode="in")))


def approx_EDV(G, A):
    influence = len(A)

    neighbourhood_excl_A = set()
    edgelist = G.get_edgelist()
    for v in A:
        neighbourhood_excl_A |= set(G.neighbors(v))  # out-neighbours!
    neighbourhood_excl_A -= set(A)

    for v in neighbourhood_excl_A:
        edgeprob = 1
        for node in A:

            if (node, v) in edgelist or (v, node) in edgelist:
                edgeprob *= 1 - weight[v]

        influence += 1 - edgeprob

    return influence

Influence_single ={}

for line in open("facebookinfluence_single"):
    u, v = line.split()
    Influence_single[int(u)] = float(v)


rd = {}
for line in open("facebookrd.txt"):
    u,v = line.split("(")
    x,y = v.split(",")
    z,w = y.split(")")
    a,b =line.split(") ")
    rd[(int(x),int(z))] = float(b)





K = 20
for i in range(30):


    problem = Problem(g, Influence_single, weight, k=K, variables_range=list(range(g.vcount())))
    evo = Evolution(problem, g.vcount(), Influence_single, rd)
    evol = evo.evolve()
    func = [i.objectives for i in evol]
    S = [i.features for i in evol]

    Spread = [1/i[0] for i in func]
    Variance = [i[1] for i in func]
    num = g.vcount()
    f = open("Rdpsoresult.txt", "a")
    f.write("---------------------\n")
    f.write(str(num) + " nodes " + str(K) + ' seeds \n')
    f.write("Seed nodes = " + str(S) + '\n')
    f.write("Spread of seed = " + str(Spread) + "\n")
    f.write("Variance = " + str(Variance) + "\n")
    f.close()
