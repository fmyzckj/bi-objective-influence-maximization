import copy
import random
import collections

def remove_duplicates(temp, tempall):
    temp1 = copy.deepcopy(temp)
    len_nodes = [len(temp[i]) for i in range(len(temp))]
    arr = []
    for i in range(len(temp)):
        for x in temp[i]:
            arr.append(x)

    dup_node = [item for item, count in collections.Counter(arr).items() if count > 1]

    for val in dup_node:
        bool_val = []
        for i in range(len(temp)):
            if val in temp[i]:
                bool_val.append(True)
            else:
                bool_val.append(False)
        T_index = [x for x in range(len(bool_val)) if bool_val[x] == True]
        preserve = random.choice(T_index)
        for j in range(len(temp)):
            if val in temp[j] and j != preserve:
                temp[j].remove(val)
    return temp

if __name__ == "__main__":
    temp = [[1, 2, 3, 5], [3, 4, 5], [5, 7, 8], [2, 3, 4]]
    tempall = [1, 2, 3, 4, 5, 7, 8]
    res = remove_duplicates(temp, tempall)
    print(res)




#for val in dup_node:
   # indicies = [i for i, x in enumerate(arr) if x == val]
    #rand_idx = random.choice(indicies)
    # remove
