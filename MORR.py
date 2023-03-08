import numpy as np
import random
import time
import argparse
import multiprocessing as mp
import sys
import math
from IC_single import IC_single
from igraph import *
import matplotlib.pyplot as plt

def attemptActivate(node:int,weight:float)->bool:
    possible=random.random()
    if(0<=possible<=weight):
        return True
    else:
        return False

class Edge():
    def __init__(self,outnode:int,innode:int,weight:float):
        self.outnode=outnode
        self.innode=innode
        self.weight=weight

def justgetRR_IC(nodeV, outDict):
    reverse_reachable_set=set()
    activeSet=set()
    nodeSet=[nodeV]
    for node in nodeSet:
        activeSet.add(node)
        reverse_reachable_set.add(node)
    while activeSet.__len__()!=0:
        newActiveSet=set()
        for node in activeSet:
            neighbours=outDict.get(node,[])
            #加个log
            for edge in neighbours:
                if edge.innode not in reverse_reachable_set and edge.innode not in newActiveSet and  attemptActivate(edge.innode,edge.weight):
                    newActiveSet.add(edge.innode)
        activeSet.clear()
        activeSet=newActiveSet
        reverse_reachable_set=reverse_reachable_set.union(newActiveSet)
    return reverse_reachable_set

def initReverseGraph(graphPath,weight):
    # graphPath="D:\\courseStation\\CS303\\Project2\\network.txt"
    # seedPath="D:\\courseStation\\CS303\\Project2\\network_seeds.txt"
    #构造图
    graphFile=open(graphPath,mode="r")
    str=graphFile.read()
    graphFile.close()
    str=str.strip()
    strsplit=str.split("\n")
    nodes = []
    edges = 0

    outDict={}
    #inDict={}
    for i in range(0,strsplit.__len__()):
        start,end = strsplit[i].split(" ")
        start=int(start)
        end=int(end)
        nodes.append(start)
        nodes.append(end)
        edges += 1

        #反向边
        edge = Edge(end, start, weight[end])
        #这是正向边
        #edge=Edge(start,end,weight)
        outNodeEdges=outDict.setdefault(end, [])
        #inNodeEdges=inDict.setdefault(start, [])
        outNodeEdges.append(edge)
        #inNodeEdges.append(edge)
    nodes = list(set(nodes))
    print(len(nodes),edges)
    nodenum = len(nodes)
    edgenum = edges
    return nodenum,outDict,nodenum,edgenum


def nodeSelection_revise(setR,k,nodeNum):

    skset=[]
    nodeAndReachableMap=dict()
    nodeLengthMap = dict()
    # i=0
    # setR_len=len(setR)
    for rrindex in range(0,len(setR)):
        currentRR=setR[rrindex]
        for node in currentRR:
           # nodeCover[node]+=1
            if node not in nodeAndReachableMap.keys():
                nodeAndReachableMap[node]=set()
            nodeAndReachableMap[node].add(rrindex)
    for node in nodeAndReachableMap:
        nodeLengthMap[node]=len(nodeAndReachableMap[node])

    # for node in nodeAndReachableMap.keys():
    #     nodeCover[node]=len(nodeAndReachableMap[node])

    for i in range(0,k):
        max_node=None
        maxNodeCoverNum=-1
        for node in  nodeLengthMap:
            coverNum=nodeLengthMap[node]
            if coverNum>maxNodeCoverNum:
                maxNodeCoverNum=coverNum
                max_node=node
        if(max_node !=None):
            skset.append(max_node)
            #print(max_node)
            #数组复制
            for rr_index in nodeAndReachableMap[max_node]:
                currentRR=setR[rr_index]
            #对于每一个被max_node覆盖到的rr，删除
                for node in currentRR:
                    if(node==max_node):
                        continue
                    nodeLengthMap[node]-=1#其它节点删除rr的影响
                    nodeAndReachableMap[node].remove(rr_index)#在node列表中删除rr
            del[nodeAndReachableMap[max_node]]
            del[nodeLengthMap[max_node]]
        else:
            while 1:
                nextNode=random.randint(0,nodeNum-1)
                if(nextNode not in skset):
                    skset.add(nextNode)
                    break

    return skset

def getRRs(nodeNum,outDict,loopnum):
    setR=[]
    for i in range(loopnum):
        nodeV=random.randint(0,nodeNum-1)
        currentReachableSet=justgetRR_IC(nodeV,outDict)
        setR.append(currentReachableSet)

    return setR

def imp(weight):
    time_start=time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default='twitter/BA1000.edgelist')
    parser.add_argument('-k', '--seedNum', type=int, default=110)
    args = parser.parse_args()
    file_name = args.file_name
    seedNum = args.seedNum
    # 1.ℓ = ℓ · (1 + log 2 / log n);
    # 2.R = Sampling(G, k, ε, ℓ);
    #跳过
    graphPath = file_name
    nodes, outDict, nodenum, edgenum=initReverseGraph(graphPath,weight)
    setR = getRRs(nodes, outDict, int(200*nodes))

    setSk=nodeSelection_revise(setR,seedNum,nodes)


    #for node in setSk:
        #print(node)
    sys.stdout.flush()
    return setSk,seedNum

if __name__ == '__main__':
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
        weight[node] = 1/(len(g.neighbors(node, mode="in")))




    Spread = []
    Variance = []
    SeedSet = []
    Inversespread = []
    Variancetemp = []
    Spreadtemp = []

    #time_start=time.time()
    num = g.vcount()
    Set, k = imp(weight)
    K = 10

    S = list(Set)

    for i in range(k-K+1):

        s,v = IC_single(g, S[i:i+K],weight)
        Spread.append(s)
        Inversespread.append(1/s)
        Variance.append(v)




        print("For the value of k = ", K)
        print('\nRRsetsmodify\n')
        print('Spread of seed = ', 1/s)
        print('Variance = ', v)

        f = open("RRmodifyresult.txt", "a")
        f.write("---------------------\n")
        f.write(str(num) + " nodes " + str(K) + ' seeds \n')
        f.write("Seed nodes = " + str(S) + '\n')
        f.write("Spread of seed = " + str(Inversespread) + "\n")
        f.write("Variance = " + str(Variance) + "\n")
        f.close()


    fig = plt.scatter(Inversespread, Variance)

    plt.xlabel('Spread', fontsize=15)
    plt.ylabel('Variance', fontsize=15)

    plt.savefig("RRsetsmodify"+str(num) + 'nodes' + str(K) + 'seeds' + "fig.png")
    plt.show()
    #fig2 = plt.scatter(list(range(len(Spread))),Inversespread)
   # plt.show()
    #fig3 = plt.scatter(list(range(len(Spread))),Variance)
   # plt.show()
    #time_end=time.time()
    #print("花费时间:",time_end-time_start)