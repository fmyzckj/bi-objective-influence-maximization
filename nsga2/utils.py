from nsga2.population import Population
import random
import copy

class NSGA2Utils:

    def __init__(self, problem, Nodes , num_of_individuals=100,
                 num_of_tour_particips=2, tournament_prob=0.9):

        self.problem = problem
        self.num_of_individuals = num_of_individuals
        self.num_of_tour_particips = num_of_tour_particips
        self.tournament_prob = tournament_prob
        self.num_of_nodes = Nodes

    def create_initial_population(self):
        population = Population()
        for _ in range(self.num_of_individuals):
            individual = self.problem.generate_individual()
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

    def create_children(self, population):
        children = []
        while len(children) < len(population):
            parent1 = self.__tournament(population)
            parent2 = parent1
            while parent1 == parent2:
                parent2 = self.__tournament(population)
            child1, child2 = self.__crossover(parent1, parent2)
            self.__mutate(child1)
            self.__mutate(child2)
            self.problem.calculate_objectives(child1)
            self.problem.calculate_objectives(child2)
            children.append(child1)
            children.append(child2)

        return children

    def __crossover(self, individual1, individual2):
        child1 = self.problem.generate_individual()
        child2 = self.problem.generate_individual()
        num_of_features = len(child1.features)
        crossover_num = int(0.1*num_of_features)
        if crossover_num == 0:
            crossover_num = 1
        genes_indexes = random.sample(list(range(num_of_features)), crossover_num)
        x = copy.deepcopy(individual1.features)
        y = copy.deepcopy(individual2.features)

        for i in range(len(genes_indexes)):
            temp = x[genes_indexes[i]]
            x[genes_indexes[i]] = y[genes_indexes[i]]
            y[genes_indexes[i]] = temp

        child1.features = list(set(x))
        child2.features = list(set(y))
        while len(child1.features) != num_of_features:
            child1.features.append(random.choice(range(self.num_of_nodes)))
            child1.features = list(set(child1.features))
        while len(child2.features) != num_of_features:
            child2.features.append(random.choice(range(self.num_of_nodes)))
            child2.features = list(set(child2.features))
        return child1, child2

    def __mutate(self, child):
        num_of_features = len(child.features)
        mute_num = int(0.1 * num_of_features)
        if mute_num == 0:
            mute_num = 1
        index = random.sample(list(range(num_of_features)), mute_num)
        delete_gene = []
        for i in range(len(index)):
            delete_gene.append(child.features[index[i]])
        for i in range(len(index)):
            child.features.remove(delete_gene[i])
        while len(child.features) != num_of_features:
            child.features.append(random.choice(range(self.num_of_nodes)))
            child.features = list(set(child.features))

    '''def __get_delta(self):
        u = random.random()
        if u < 0.5:
            return u, (2*u)**(1/(self.mutation_param + 1)) - 1
        return u, 1 - (2*(1-u))**(1/(self.mutation_param + 1))'''

    def __tournament(self, population):
        participants = random.sample(population.population, self.num_of_tour_particips)
        best = None
        for participant in participants:
            if best is None or (self.crowding_operator(participant, best) == 1 and self.__choose_with_prob(self.tournament_prob)):
                best = participant

        return best

    def __choose_with_prob(self, prob):
        if random.random() <= prob:
            return True
        return False
