#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import random
import numpy
import sys

from moeadpy.moead import MOEAD
from EDV import approx_EDV
import copy

from deap import base
from deap import creator
from deap import tools
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

IND_INIT_SIZE = 20
MAX_ITEM = 50 #f1最大
MAX_WEIGHT = 50 #f2最大
NBR_ITEMS = 1000 #x取值范围


NGEN = 50 #迭代此处
Maxeva = 50000
MU = 100 #种群数量
LAMBDA = 2
CXPB = 0.7 #交叉概率
MUTPB = 0.2 #变异概率

# Create random items and store them in the items' dictionary.
items = {}
for i in range(NBR_ITEMS):
    items[i] = (random.randint(1, 10), random.uniform(0, 100))



def geteval(individual):

    influence,variance = approx_EDV(g,Influence_single,individual,weight)

    return influence, variance


def evalKnapsack(individual):    
    weight = 0.0
    value = 0.0
    for item in individual:
        weight += items[item][0]
        value += items[item][1]
    if len(individual) > MAX_ITEM or weight > MAX_WEIGHT:
        return 1e30, 0.0 # Ensure overweighted bags are dominated
    return weight, value

def evalKnapsackBalanced(individual):
    """
    Variant of the original weight-value knapsack problem with added third object being minimizing weight difference between items.
    """
    weight, value = evalKnapsack(individual)
    balance = 0.0
    for a,b in zip(individual, list(individual)[1:]):
        balance += abs(items[a][0]-items[b][0])
    if len(individual) > MAX_ITEM or weight > MAX_WEIGHT:
        return weight, value, 1e30 # Ensure overweighted bags are dominated
    return weight, value, balance

def cxSet(ind1, ind2):
    """Apply a crossover operation on input sets. The first child is the
    intersection of the two sets, the second child is the difference of the
    two sets.
    """
    temp = set(ind1)                # Used in order to keep type
    ind1 &= ind2                    # Intersection (inplace)
    ind2 ^= temp                    # Symmetric Difference (inplace)
    return ind1, ind2

def cross(indi1,indi2):
    num_of_features = len(indi1)
    crossover_num = int(0.1 * num_of_features)
    if crossover_num == 0:
        crossover_num = 1
    genes_indexes = random.sample(list(range(num_of_features)), crossover_num)
    x = copy.deepcopy(indi1)
    y = copy.deepcopy(indi2)

    for i in range(len(genes_indexes)):
        temp = x[genes_indexes[i]]
        x[genes_indexes[i]] = y[genes_indexes[i]]
        y[genes_indexes[i]] = temp

    child1 = list(set(x))
    child1 = creator.Individual(child1)
    child2 = list(set(y))
    child2 = creator.Individual(child2)
    while len(child1) != num_of_features:
        child1.append(random.choice(range(NBR_ITEMS)))
        child1 = list(set(child1))
        child1 = creator.Individual(child1)
    while len(child2) != num_of_features:
        child2.append(random.choice(range(NBR_ITEMS)))
        child2 = list(set(child2))
        child2 = creator.Individual(child2)

    return child1, child2
    
def mutSet(individual):
    """Mutation that pops or add an element."""
    if random.random() < 0.5:
        if len(individual) > 0:     # We cannot pop from an empty set
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(NBR_ITEMS))
    return individual,

def mutation(child):
    num_of_features = len(child)
    mute_num = int(0.1 * num_of_features)
    if mute_num == 0:
        mute_num = 1
    index = random.sample(list(range(num_of_features)), mute_num)
    delete_gene = []
    for i in range(len(index)):
        delete_gene.append(child[index[i]])
    for i in range(len(index)):
        child.remove(delete_gene[i])
    while len(child) != num_of_features:
        child.append(random.choice(range(NBR_ITEMS)))
        child = list(set(child))
        child = creator.Individual(child)
    return child

def main(objectives=2, seed=64):
    random.seed(seed)

    # Create the item dictionary: item name is an integer, and value is 
    # a (weight, value) 2-uple.
    if objectives == 2:
        creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
    elif objectives == 3:
        creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0, -1.0))
    else:
        print("No evaluation function available for", objectives, "objectives.")
        sys.exit(-1)

        
    creator.create("Individual", list, fitness=creator.Fitness)

    toolbox = base.Toolbox()

    # Attribute generator
    toolbox.register("attr_item", random.randrange, NBR_ITEMS)

    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, 
                     toolbox.attr_item, IND_INIT_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    if objectives == 2:
        toolbox.register("evaluate", geteval)
    elif objectives == 3:
        toolbox.register("evaluate", evalKnapsackBalanced)
    else:
        print("No evaluation function available for", objectives, "objectives.")
        sys.exit(-1)
        

    toolbox.register("mate", cross)
    toolbox.register("mutate", mutation)
    toolbox.register("select", tools.selNSGA2)

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()

    stats = {}
    def lambda_factory(idx):
        return lambda ind: ind.fitness.values[idx]                

    fitness_tags = ["Influence", "Variance"]
    for tag in fitness_tags:
        s = tools.Statistics( key=lambda_factory(
                    fitness_tags.index(tag)
                ))
        stats[tag] = s

    mstats = tools.MultiStatistics(**stats)
    mstats.register("avg", numpy.mean, axis=0)
    mstats.register("std", numpy.std, axis=0)
    mstats.register("min", numpy.min, axis=0)
    mstats.register("max", numpy.max, axis=0)

    ea = MOEAD(pop, toolbox, MU, CXPB, MUTPB, maxEvaluations=Maxeva ,stats=mstats, halloffame=hof, nr=LAMBDA)
    pop = ea.execute()
    
    return pop, stats, hof
                 
if __name__ == "__main__":
    objectives = 2
    seed = 64
    if len(sys.argv) > 1:
        seed = int(sys.argv[1])
    if len(sys.argv) > 2:
        objectives = int(sys.argv[2])

    pop,stats,hof = main(objectives)

    pop = [str(p) +" "+ str(p.fitness.values) for p in pop]
    hof = [str(h) +" "+ str(h.fitness.values) for h in hof]
    print("POP:")
    print("\n".join(pop))

    print("PF:")
    print("\n".join(hof))
