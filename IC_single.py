import copy
import time

import numpy as np
import ray

from removedup import remove_duplicates


def IC_single_para(g, S, weight,mc=10000):

    mcspread = []  #new node for each spread for each node each round
    for i in range(len(S)):
        mcspread.append([])
    start =time.time()
    eachspread = ray.get([Monte_Carol.remote(S,weight,g) for i in range(mc)])

    for sets in eachspread:
        for j in range(len(S)):
            mcspread[j].append(len(sets[j]))
    allspread = []
    for j in range(len(S)):
        allspread.append(sum(mcspread[j]) / mc)
    variance = np.var(allspread)
    spread = sum(allspread)

    return (1 / spread, variance)

@ray.remote
def Monte_Carol(S,weight,g):
    eachspread = []
    roundspread = []

    # Simulate propagation process
    new_active, A = S[:], S[:]

    for node in S:
        eachspread.append([node])
        roundspread.append([node])

    while new_active:

        # For each newly active node, find its neighbors that become activated
        new_ones = []
        temp = []  # save temp spread for each node
        tempall = []  # save all spread node in this round, no repeat
        x = []
        new_active = []
        for node in S:
            temp.append([])

        for j in range(len(S)):
            for node in roundspread[j]:
                # np.random.seed(j)
                # print(g.neighbors(node, mode="out"))
                # print(g.neighbors(node, mode="in"))
                for neighbor in g.neighbors(node, mode="out"):
                    if np.random.uniform(0, 1) < weight[neighbor]:
                        temp[j].append(neighbor)
            # success = np.random.uniform(0,1,len(g.neighbors(node, mode="out"))) < p
            # temp[j] += list(np.extract(success, g.neighbors(node, mode="out")))

        for j in range(len(S)):
            temp[j] = list(set(temp[j]))

        influenced_nodes_cur_iter = copy.deepcopy(temp)

        for j in range(len(S)):  # remove former activated nodes
            for node in influenced_nodes_cur_iter[j]:
                if node in A:
                    temp[j].remove(node)

        for j in range(len(S)):  # record all new activated nodes this round, no repeat
            for y in temp:
                x += y

        tempall = list(set(x))

        temp = remove_duplicates(temp, tempall)

        roundspread = temp
        for j in range(len(S)):
            for node in roundspread[j]:
                eachspread[j].append(node)

        x = []

        for j in range(len(S)):  # record all new activated nodes this round, no repeat
            for z in temp:
                x += z

        new_active = list(set(x))

        A += new_active

    return eachspread






def IC_single(g,S,weight,mc=50):
    """
    Input:  graph object, set of seed nodes, propagation probability
            and the number of Monte-Carlo simulations
    Output: average number of nodes influenced by the seed nodes
    """
    
    # Loop over the Monte-Carlo Simulations
    spread = []
    #spread for each node


    mcspread = []#new node for each spread for each node each round
    for i in range(len(S)):
        mcspread.append([])



    for i in range(mc):
        eachspread = []
        roundspread = []
        
        # Simulate propagation process      
        new_active, A = S[:], S[:]

        for node in S:
            eachspread.append([node])
            roundspread.append([node])

        while new_active:

            # For each newly active node, find its neighbors that become activated
            new_ones = []
            temp = []  # save temp spread for each node
            tempall = [] # save all spread node in this round, no repeat
            x = []
            new_active = []
            for node in S:
                temp.append([])

            for j in range(len(S)):
                for node in roundspread[j]:
                    #np.random.seed(j)
                    #print(g.neighbors(node, mode="out"))
                    #print(g.neighbors(node, mode="in"))
                    for neighbor in g.neighbors(node, mode = "out"):
                        if np.random.uniform(0,1) < weight[neighbor]:
                            temp[j].append(neighbor)
                   # success = np.random.uniform(0,1,len(g.neighbors(node, mode="out"))) < p
                   # temp[j] += list(np.extract(success, g.neighbors(node, mode="out")))

            for j in range(len(S)):
                temp[j] = list(set(temp[j]))

            influenced_nodes_cur_iter = copy.deepcopy(temp)

            for j in range(len(S)):  #remove former activated nodes
                for node in influenced_nodes_cur_iter[j]:
                    if node in A:
                        temp[j].remove(node)

            for j in range(len(S)): #record all new activated nodes this round, no repeat
                for y in temp:
                    x += y

            tempall = list(set(x))

            temp = remove_duplicates(temp,tempall)

            roundspread = temp
            for j in range(len(S)):
                for node in roundspread[j]:
                    eachspread[j].append(node)


            x = []

            for j in range(len(S)): #record all new activated nodes this round, no repeat
                for z in temp:
                    x += z


            new_active = list(set(x))

            A += new_active


        for j in range(len(S)):
            mcspread[j].append(len(eachspread[j]))
    allspread = []
    for j in range(len(S)):
        allspread.append(sum(mcspread[j])/mc)
    variance = np.var(allspread)
    spread = sum(allspread)

        
    return(1/spread,variance)