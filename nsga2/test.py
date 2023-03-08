from igraph import *


def dominates(individual,other_individual):
    and_condition = True
    or_condition = False
    for first, second in zip(individual, other_individual):
        and_condition = and_condition and first <= second
        or_condition = or_condition or first < second
    return (and_condition and or_condition)

indi1 = [1/123,111]
indi2 = [1/222,222]

print(dominates(indi1,indi2))

