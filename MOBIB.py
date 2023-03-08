from improvednsga2.problem import Problem
from improvednsga2.evolution import Evolution
import matplotlib.pyplot as plt
import math
from IC_single import IC_single
from igraph import *
import time

edges = []
nodes = []
for line in open("twitter/BA1000.edgelist"):
    u, v = line.split()
    edges.append((int(u), int(v)))
    nodes.append(int(u))
    nodes.append(int(v))
nodes = list(set(nodes))

g = Graph(edges)
weight = {}


for node in nodes:
    weight[node] = 1 / (len(g.neighbors(node, mode="in")))



Influence_single ={}

for line in open("1000influence_single"):
    u, v = line.split()
    Influence_single[int(u)] = float(v)


rd = {}
for line in open("1000rd.txt"):
    u,v = line.split("(")
    x,y = v.split(",")
    z,w = y.split(")")
    a,b =line.split(") ")
    rd[(int(x), int(z))] = float(b)






#K = [int(x) for x in input().split()]
K = 20
generations = 1000
muterate = 0.8
for i in range(1):
    #start = time.time()

    problem = Problem(g, Influence_single, weight, k=K, variables_range=list(range(g.vcount())))

    evo = Evolution(problem, g.vcount(), 1, Influence_single, rd, num_of_generations = generations, mutaterate = muterate)

    evol = evo.evolve()
    #print("time",time.time()-start)
    func = [i.objectives for i in evol]
    S = [i.features for i in evol]

    '''print("For the value of k = ", i)
    print('\nImprovedNSGAII\n')
    print('Seed Nodes = ', S)
    print('Spread of seed = ', [1/i[0] for i in func])
    print('Variance = ', [i[1] for i in func])'''
    Spread = [1/i[0] for i in func]
    Variance = [i[1] for i in func]
    num = g.vcount()
    f = open("ImprovedNSGAII2000.txt", "a")
    f.write("---------------------\n")
    f.write(str(num) + " nodes " + str(K) + ' seeds +'+str(muterate)+"rate"+str(generations)+"generation\n")
    f.write("Seed nodes = " + str(S) + '\n')
    f.write("Spread of seed = " + str(Spread) + "\n")
    f.write("Variance = " + str(Variance) + "\n")
    f.close()

