from improvednsga2.utils import NSGA2Utils
from improvednsga2.population import Population
import ray
import time


class Evolution:

    def __init__(self, problem, Nodes, choosingrate, influence_single, rd, num_of_generations=1000, num_of_individuals=100, num_of_tour_participants=2, tournament_prob=0.9, mutaterate = 0.6):
        self.utils = NSGA2Utils(problem, Nodes, choosingrate, influence_single, rd, num_of_individuals, num_of_tour_participants, tournament_prob, mutaterate)
        self.population = None
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals
        self.Nodes = Nodes
        self.muterate = mutaterate

    def evolve(self):
        self.population = self.utils.create_initial_population()
        self.utils.fast_nondominated_sort(self.population)
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)

        children = self.utils.create_children(self.population)

        #returned_population = None
        f = open("ImprovedNSGAII"+str(self.Nodes)+"nodes"+str(self.muterate)+"rate"+"each1generation.txt", "a")
        for i in range(self.num_of_generations):
            start = time.time()

            self.population.extend(children)

            self.utils.fast_nondominated_sort(self.population)

            new_population = Population()
            front_num = 0

            while len(new_population) + len(self.population.fronts[front_num]) < self.num_of_individuals:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1

            self.utils.calculate_crowding_distance(self.population.fronts[front_num])

            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)

            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals-len(new_population)])

            #returned_population = self.population
            self.population = new_population
            self.utils.fast_nondominated_sort(self.population)
            for front in self.population.fronts:
                self.utils.calculate_crowding_distance(front)
            children = self.utils.create_children(self.population)
            print("generation",i)
            print(len(self.population.fronts[0]))
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
