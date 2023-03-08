from rdpso.individual import Individual
import random
from IC_single import IC_single
from EDV import approx_EDV

class Problem:

    def __init__(self,g ,influence_single,weight, k, variables_range):
        self.k = k
        self.variables_range = variables_range
        self.g = g
        self.weight = weight
        self.influence_single = influence_single

    def generate_individual(self):
        individual = Individual()
        individual.features = random.sample(self.variables_range, self.k)
        individual.binaryfeatures = self.real_to_binary(individual.features)
        return individual

    def get_k(self):
        return self.k

    def calculate_objectives(self, individual):
        individual.objectives = approx_EDV(self.g, self.influence_single, individual.features, self.weight, )

    def binary_to_real(self, binary):
        real = []
        for i in range(len(binary)):
            if binary[i] == 1:
                real.append(i)
        return real

    def real_to_binary(self,real):
        binary = []
        for i in range(len(self.variables_range)):
            if i in real:
                binary.append(1)
            else:
                binary.append(0)

        return binary
