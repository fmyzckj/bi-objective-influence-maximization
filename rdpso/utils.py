from rdpso.population import Population
from rdpso.individual import Individual
import random
import copy

class NSGA2Utils:

    def __init__(self, problem, Nodes, Influence_single, rd , num_of_individuals=100):

        self.problem = problem
        self.num_of_individuals = num_of_individuals
        self.Influence_single = Influence_single
        self.rd = rd
        self.num_of_nodes = Nodes
        self.k = self.problem.get_k()
        self.cluster = None

    def generate_individual(self):
        individual = Individual()
        cluster = self.rd_clustering()
        individual.features = []
        if len(list(cluster.keys())) >= self.k:
            cluster_list = random.sample(list(cluster.keys()),self.k)
            for i in range(self.k):
                individual.features.append(random.choice(cluster[cluster_list[i]]))
        else:
            for i in range(len(list(cluster.keys()))):
                individual.features.append(random.choice(cluster[i]))
            while len(individual.features) != self.k:
                individual.features.append(random.choice(cluster[random.randint(0,len(list(cluster.keys()))-1)]))
                individual.features = list(set(individual.features))

        individual.binaryfeatures = self.real_to_binary(individual.features)
        return individual

    def rd_clustering(self):
        cluster = {}
        in_cluster = {}
        for i in range(self.num_of_nodes):
            in_cluster[i] = False
        cluster_num = 0
        for i in range(self.num_of_nodes):
            lowest_rd = 2
            j_num = 0
            if in_cluster[i] == False:
                for j in range(self.num_of_nodes):
                    if i != j:
                        if self.rd[(i,j)] < lowest_rd:
                            lowest_rd = self.rd[(i,j)]
                            j_num = j
                if in_cluster[j_num] == False:
                    in_cluster[i] = cluster_num
                    in_cluster[j_num] = cluster_num
                    cluster[cluster_num] = []
                    cluster[cluster_num].append(i)
                    cluster[cluster_num].append(j_num)
                    cluster_num += 1
                else:
                    in_cluster[i] = in_cluster[j_num]
                    cluster[in_cluster[j_num]].append(i)
        self.cluster = cluster
        return cluster



    def create_initial_population(self):
        population = Population()
        for _ in range(self.num_of_individuals):
            individual = self.generate_individual()
            individual.velo = [0]*self.num_of_nodes
            self.problem.calculate_objectives(individual)
            population.append(individual)
        return population

    def fast_nondominated_sort(self, population):
        population.fronts = [[]]
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                individual.rank = 0
                population.fronts[0].append(individual)
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        temp.append(other_individual)
            i = i+1
            population.fronts.append(temp)

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                front.sort(key=lambda individual: individual.objectives[m])
                front[0].crowding_distance = 10**9
                front[solutions_num-1].crowding_distance = 10**9
                m_values = [individual.objectives[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0: scale = 1
                for i in range(1, solutions_num-1):
                    front[i].crowding_distance += (front[i+1].objectives[m] - front[i-1].objectives[m])/scale

    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
            ((individual.rank == other_individual.rank) and (individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1

    def binary_to_real(self, binary):
        real = []
        for i in range(len(binary)):
            if binary[i] == 1:
                real.append(i)

        return real

    def real_to_binary(self,real):
        binary = []
        for i in range(self.num_of_nodes):
            if i in real:
                binary.append(1)
            else:
                binary.append(0)

        return binary

    def calculate(self, individual):
        self.problem.calculate_objectives(individual)

    def legalize(self,individual):
        if len(individual.features) > self.k:
            individual.features = random.sample(individual.features, self.k)
        if len(individual.features) < self.k:
            while len(individual.features) != self.k:
                less_num = self.k - len(individual.features)
                if len(list(self.cluster.keys())) >= less_num:
                    cluster_list = random.sample(list(self.cluster.keys()), less_num)
                    for i in range(less_num):
                        individual.features.append(random.choice(self.cluster[cluster_list[i]]))
                    individual.features = list(set(individual.features))
                else:
                    for i in range(len(list(self.cluster.keys()))):
                        individual.features.append(random.choice(self.cluster[i]))
                    while len(individual.features) != self.k:
                        individual.features.append(random.choice(self.cluster[random.randint(0, len(list(self.cluster.keys())) - 1)]))
                        individual.features = list(set(individual.features))
        self.problem.calculate_objectives(individual)











    '''def __get_delta(self):
        u = random.random()
        if u < 0.5:
            return u, (2*u)**(1/(self.mutation_param + 1)) - 1
        return u, 1 - (2*(1-u))**(1/(self.mutation_param + 1))'''



    def __choose_with_prob(self, prob):
        if random.random() <= prob:
            return True
        return False
