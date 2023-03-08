import numpy as np
import time




def approx_EDV(G, Influence_single, A, weight):
    influence = len(A)
    neighbourhood_excl_A = set()
    #record1 = time.time()
    #edgelist = G.get_edgelist()
    #record2 = time.time()
    for v in A:
        neighbourhood_excl_A |= set(G.neighbors(v))  # out-neighbours!
    neighbourhood_excl_A -= set(A)
    #record3 = time.time()

    for v in neighbourhood_excl_A:
        edgeprob = 1
        for node in A:
            if v in G.neighbors(node):
                edgeprob *= 1 - weight[v]

        influence += 1 - edgeprob
    #record4 = time.time()


    vspread = []

    for v in A:
        vspread.append(Influence_single[v])
    variance = np.var(vspread)
    #record5 = time.time()
    ''' print("1", record2 - record1)
    print("2", record3 - record2)
    print("3", record4 - record3)
    print("4", record5 - record4)'''

    return 1/influence, variance
