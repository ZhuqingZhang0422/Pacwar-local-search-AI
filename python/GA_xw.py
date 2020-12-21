import _PyPacwar
import numpy
# simple hill climbing
import random
import sys
import os
from collections import defaultdict
import util_xw as util
import threading  # multiple thread


class GA():
    def __init__(self, initialparent, sites=[[0, 4], [4, 20], [20, 23], [23, 26], [26, 38], [38, 50]]):
        self.start = initialparent  # which is the initial father list of candidiates the candidate should be in a list [[,,]]
        self.current_population = [[i, 0] for i in self.start]  # i is the list# [sequence, score]
        self.sites = sites

    def fitness(self, multiple=4):  # take the longest time now
        # take the current population and then combat between the generation and return the best
        if multiple == 1:
            for index_i in range(len(self.current_population)):
                # i=self.current_population[index_i][0]
                for index_j in range(index_i + 1, len(self.current_population)):
                    # j=self.current_population[index_j][0]

                    self.score_function(index_i, index_j)
        else:  # multiple thread
            # 4 thread
            total_len = len(self.current_population)
            regions = [[0, int(total_len // 4)], [int(total_len // 4), 2 * int(total_len // 4)],
                       [2 * int(total_len // 4), 3 * int(total_len // 4)], [3 * int(total_len // 4), total_len]]
            t0 = threading.Thread(target=self.subfitness, args=(regions[0],))
            t1 = threading.Thread(target=self.subfitness, args=(regions[1],))
            t2 = threading.Thread(target=self.subfitness, args=(regions[2],))
            t3 = threading.Thread(target=self.subfitness, args=(regions[3],))
            t0.start()
            t1.start()
            t2.start()
            t3.start()
            t0.join()
            t1.join()
            t2.join()
            t3.join()

    def subfitness(self, index_i_position):
        for index_i in range(index_i_position[0], index_i_position[1]):
            for index_j in range(index_i + 1, len(self.current_population)):
                #    j=self.current_population[index_j][0]

                self.score_function(index_i, index_j)

    def score_function(self, index_i, index_j):
        ## can be changed based on different principle
        i = self.current_population[index_i][0]
        j = self.current_population[index_j][0]
        # print('Now is battling')
        # print(i)
        # print(j)
        if i != j:
            result_i, result_j = util.outcome_of_duel(i, j)
            # print(result_i)
            # print(result_j)
            self.current_population[index_i][1] += result_i
            self.current_population[index_j][1] += result_j

    def selection(self, n):
        self.current_population.sort(key=lambda x: x[1], reverse=1)  # from large to small
        while len(self.current_population) > n:
            self.current_population.pop()

    def run(self, generation_limit=100, limitsize=100,selecnumber=3, mutated_sites_number=1, mutation_possiblility_for_single=0.2,subling_limit=10):
        # after initiate the problem execute this run
        current_generation = 0
        combination_possibility = util.calculate_combine_pattern(len(self.sites))
        while generation_limit != 0:
            print('generation' + str(current_generation),' ;length=',str(len(self.current_population)))
            if len(self.current_population)>limitsize:
                # shrink
                pk_target = [[1] * 50, [3] * 50]
                for index_i, i in enumerate(self.current_population):
                    for j in pk_target:
                        result1, result2 = util.outcome_of_duel(i[0], j)
                        # print(result_i)
                        # print(result_j)
                        self.current_population[index_i][1] += result1
                self.current_population.sort(key=lambda x:x[1],reverse=1)
                n=len(self.current_population)
                while n>limitsize:
                    self.current_population.pop()
                    n-=1
            self.fitness()  # battle and update score
            util.record(current_generation, self.current_population, append='all', print_score=1)
            self.selection(selecnumber)  # select who can then crossover 3
            util.record(current_generation, self.current_population, append='parent', print_score=1)

            # new generation by random crossover
            print('crossover')
            next_generation = []
            for i in self.current_population:
                for j in self.current_population:
                    if i != j:
                        children = util.crossover(i[0], j[0], combination_possibility, self.sites,subling_limit)
                        for child in children:
                            util.mutation(child, mutated_sites_number, mutation_possiblility_for_single)

                            if [child, 0] not in next_generation:
                                next_generation.append([child, 0])
            # self.current_population=next_generation#[(candidate,0)]
            for i in self.current_population:
                i[1]=0
            for _ in next_generation:  # [(candidate,0)]: # combine
                if _ not in self.current_population:
                    self.current_population.append(_)
            generation_limit -= 1
            current_generation += 1
        # when it break:
        self.fitness()
        util.record(current_generation, self.current_population, append='all', print_score=1)
        self.selection(selecnumber)
        util.record(current_generation, self.current_population, append='parent', print_score=1)
        util.record(current_generation, self.current_population, append='final', print_score=0)
        return self.current_population


def main():
    ones = [1] * 50
    threes = [3] * 50
    dummy = [
        '10113012101110111111111111111111120113111111111111',
        '10111111101110110011121111111121102111111101111101',
        '10111111101110111111101111111110111111111111111111',
        '10111101111111111111111111111111111111111111111113',
        '11111111111111111111111113111111111111111111111111',
        '11111111111111311111111111111111111111111111111111',
        '11111110121111111111131111111121111011111101111112',
        '10111011131110113111111111111101101111101111101101',
        '12111101111111111111111111111110011311011111111111',
        '11111110113111221111111111111111113111211131111121',
        '10111112301130111311111111111112111111131111111221',
        '11111111111111111102111111111121110111111033111111',
        '11111211112111111130111111111111111111111111111111',
        '11111131111111111111101111111111110111111112311111',
        '10111030102113111111131111111111111111110201001111',
        '11111111111113131111300111111121101120121111013111'
    ]
    start = []

    start.append(ones)
    start.append(threes)
    for i in dummy:
        start.append([int(x) for x in i])
    dir = 'testnew'
    os.mkdir(dir)
    os.chdir(r'testnew')
    solution = GA(start)
    res = solution.run(generation_limit=10000,limitsize=100, selecnumber=12,subling_limit=9)
    print(res)


if __name__ == "__main__": main()
