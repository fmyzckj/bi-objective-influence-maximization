from improvednsga2.individual import Individual
import random
#from IC_single import IC_single_para
#from IC_single import IC_single
from EDV import approx_EDV
#import time

class Problem:

    def __init__(self,g ,influence_single, weight, k, variables_range):
        self.k = k
        self.variables_range = variables_range
        self.g = g
        self.weight = weight
        self.influence_single = influence_single

    def generate_individual(self):
        individual = Individual()
        individual.features = random.sample(self.variables_range, self.k)
        return individual

    def calculate_objectives(self, individual):
        individual.objectives = approx_EDV(self.g, self.influence_single, individual.features, self.weight,)
        #individual.objectives = IC_single(self.g, individual.features, self.weight)



