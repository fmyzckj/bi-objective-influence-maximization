from improvednsga2.problem import Problem
from improvednsga2.evolution import Evolution
import matplotlib.pyplot as plt
import math
from IC_single import IC_single
from igraph import *
import time

edges = []
nodes = []
for line in open("twitter/wiki.edgelist"):
    u, v = line.split()
    edges.append((int(u), int(v)))
    nodes.append(int(u))
    nodes.append(int(v))
nodes = list(set(nodes))

g = Graph(edges)
weight = {}


for node in nodes:
    if len(g.neighbors(node, mode="in")) != 0:
        weight[node] = 1 / (len(g.neighbors(node, mode="in")))
    else:
        weight[node] = 0


def approx_EDV(G, A):
    influence = len(A)

    neighbourhood_excl_A = set()
    for v in A:
        neighbourhood_excl_A |= set(G.neighbors(v))  # out-neighbours!
    neighbourhood_excl_A -= set(A)

    for v in neighbourhood_excl_A:
        edgeprob = 1
        for node in A:
            if v in G.neighbors(node):
                edgeprob *= 1 - weight[v]
        influence += 1 - edgeprob

    return influence

Influence_single = {}

for line in open("wikiinfluence_single"):
    u, v = line.split()
    Influence_single[int(u)] = float(v)

def calculate_rd(i, j):
    if i != j:
        union = [i, j]
    else:
        union = [i]

    rd = approx_EDV(g,union)/(Influence_single[i]+Influence_single[j])
    return rd
rd = {}
f = open("wikird.txt", "a")
y = []
double_rd = {}
'''for i in nodes:
    for j in nodes:
        if j >= i:
            y.append([i, j])

for (i,j) in y:
    start = time.time()
    rd[(i,j)] = calculate_rd(i,j)
    rd[(j,i)] = rd[(i,j)]
    f.write(str((i, j)) + " " + str(rd[i, j]) + '\n')
    f.write(str((j, i)) + " " + str(rd[i, j]) + '\n')
    print(time.time()-start)'''
for i in nodes:
    for j in nodes:
        if j >= i:
            start = time.time()
            rd[(i, j)] = calculate_rd(i, j)
            rd[(j, i)] = rd[(i, j)]
            f.write(str((i, j)) + " " + str(rd[i, j]) + '\n')
            f.write(str((j, i)) + " " + str(rd[i, j]) + '\n')
            print(time.time() - start)

f.close()