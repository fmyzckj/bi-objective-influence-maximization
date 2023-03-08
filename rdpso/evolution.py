import random
import operator
from rdpso.utils import NSGA2Utils
from rdpso.population import Population

class Evolution:

    def __init__(self, problem, Nodes, influence_single, rd, num_of_generations=1000, num_of_individuals=100):
        self.utils = NSGA2Utils(problem, Nodes, influence_single, rd, num_of_individuals)
        self.population = None
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals
        self.Nodes = Nodes

    def dominates(self, individual):
        and_condition = True
        or_condition = False
        for first, second in zip(individual.objectives, individual.plobjectives):
            and_condition = and_condition and first <= second
            or_condition = or_condition or first < second
        return (and_condition and or_condition)

    def evolve(self):
        self.population = self.utils.create_initial_population()
        f = open("rdpso"+str(self.Nodes)+"each1generation.txt", "a")

        for i in range(self.num_of_generations):

            self.utils.fast_nondominated_sort(self.population)

            for individual in self.population:
                if  individual.pl == None or self.dominates(individual):
                    individual.pl = individual.features
                    individual.plobjectives = individual.objectives
                    individual.plbinary = individual.binaryfeatures
            for individual in self.population:
                pg = random.choice(self.population.fronts[0])
                z1 = random.random()
                z2 = random.random()
                local_change = list(map(operator.sub, individual.plbinary, individual.binaryfeatures))
                x = list(map(lambda i: i * 1.495*z1, local_change))
                global_change = list(map(operator.sub, pg.binaryfeatures, individual.binaryfeatures))
                y = list(map(lambda i: i * 1.995*z2, global_change))
                velo = list(map(lambda i: i * 0.729, individual.velo))
                temp = list(map(operator.add,x,y))
                individual.velo = list(map(operator.add,temp,velo))
                temp2 = list(map(operator.add, individual.binaryfeatures, individual.velo))
                individual.binaryfeatures = []
                for i in temp2:
                    if i >= 0.5:
                        individual.binaryfeatures.append(1)
                    else:
                        individual.binaryfeatures.append(0)
                individual.features = self.utils.binary_to_real(individual.binaryfeatures)
                self.utils.legalize(individual)
            func = [i.objectives for i in self.population.fronts[0]]
            Spread = [1 / i[0] for i in func]
            Variance = [i[1] for i in func]
            print("Spreadofseed",Spread)
            print("Variance",Variance)

            f.write("---------------------\n")
            f.write(str(i) + "\n")
            f.write(str(len(Spread))+'\n')

            f.write("Spread of seed = " + str(Spread) + "\n")
            f.write("Variance = " + str(Variance) + "\n")


        self.utils.fast_nondominated_sort(self.population)


        return self.population.fronts[0]
