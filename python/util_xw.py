import numpy
import _PyPacwar
import random
import collections
from multiprocessing import Pool,Manager
import copy

def outcome_of_duel(i, j):  # i and j are in list
    (rounds, c1, c2) = _PyPacwar.battle(i, j)
    if c1 > c2:  # c1 win
        if rounds < 100:
            return 20, 0
        elif rounds < 199:
            return 19, 1
        elif rounds < 299:
            return 18, 2
        elif rounds < 500:
            return 17, 3
        elif c2 == 0 or c1 / c2 > 10:
            return 13, 7
        elif c1 / c2 > 3:
            return 12, 8
        elif c1 / c2 > 1.5:
            return 11, 9
        else:
            return 10, 10
    elif c1 == c2:
        return 10, 10
    else:  # c2 win
        if rounds < 100:
            return 0, 20
        elif rounds < 199:
            return 1, 19
        elif rounds < 299:
            return 2, 18
        elif rounds < 500:
            return 3, 17
        elif c1 == 0 or c2 / c1 > 10:
            return 7, 13
        elif c2 / c1 > 3:
            return 8, 12
        elif c2 / c1 > 1.5:
            return 9, 11
        else:
            return 10, 10
    # checked 10/11/2020

def calculate_combine_pattern(n):  # n position each position 0 or 1
    combination_possibility = []
    for i in range(2 ** n):
        a = bin(i)
        a = a[2:] if i > 0 else a[3:]
        b = i.bit_length()
        temp = '0' * (n - b) + a
        combination_possibility.append(temp)
    return combination_possibility
    # checked 10/11/2020


def crossover(parent0, parent1, combination_possibility,
              how_to_separate_gene):  # select 2 to crossover return unique child no mutation here
    ## how to crossover
    # try a dommy crossover
    # total length of the gene is 50
    # there are different
    # u v w x y z
    # u 0:4 (4) V 4:20 (16) W 20:23 (3) X: 23:26 (3) Y 26:38 (12) Z: 38:50 (12)
    # n=2**len(how_to_seperate_gene) # how many possibile child ~2**6 64 childs
    childs = []
    for i in combination_possibility:
        temp = []
        for index, gene in enumerate(i):
            if gene == '0':  # from parent0
                temp = temp + parent0[how_to_separate_gene[index][0]:how_to_separate_gene[index][1]]
            else:
                temp = temp + parent1[how_to_separate_gene[index][0]:how_to_separate_gene[index][1]]
        if temp not in childs:
            childs.append(temp)  # unique child
    # return a list of all child
    return childs
    # checked 10/11/2020


def sub_shrink(population, pk_target,winhowmany):
    win_times = collections.defaultdict(int)
    if winhowmany == -1:
        winhowmany = min(len(pk_target),winhowmany)
    for index_i,i in enumerate(population):
        for j in pk_target:
            if j!=i[0]:
                result1, result2 = outcome_of_duel(i[0], j)
                # print(result_i)
                # print(result_j)
                population[index_i][1] += result1
                win_times[index_i] += 1 if result1 >= result2 else 0  # win times
    remove_list=[]
    for i ,temp in win_times.items():
        if temp < winhowmany:  # must win winhowmany default is at least one of the parent
            remove_list.append(i)  # if win less then will be removed
    while remove_list:
        population.pop(remove_list.pop())
    return population

def shrink_the_size_of_population(population, limitsize, pk_target=None, winhowmany=-1,multiple=4):  # 2 for parent # -1 win all
    # population [[genes,0],[genes,0]]
    # the default target is the pk_target
    # this function is used to shrink the child size.
    # the principle is to compare with all pk_target and need to win most/or howmany of them
    # then filter what we want and then sort the score and select the child based on the subling limit
    # print(duplicate)
    # print('test')
    duplicate=dict()
    for i in population:
        if str(i[0]) not in duplicate:
            duplicate[str(i[0])]=1
        elif str(i[0]) in duplicate:
            print('duplicate found')
        if i[1]!=0:
            print('wrong')


    if pk_target is None:
        pk_target = [[1] * 50, [3] * 50]


    if multiple==1:
        population=sub_shrink(population, pk_target,winhowmany)
        '''
        win_times = collections.defaultdict(int)
        
        for index_i, i in enumerate(population):
            for j in pk_target:
                result1, result2 = outcome_of_duel(i[0], j)
                # print(result_i)
                # print(result_j)
                population[index_i][1] += result1
                win_times[index_i] += 1 if result1 >= result2 else 0  # win times
        for index_i, i in enumerate(population):
            if win_times[index_i] < winhowmany:  # must win winhowmany default is at least one of the parent
                population.remove(i)  # if win less then will be removed
        '''
    else: # multiple
    ## modified to multiple process


        total_len=len(population)
        regions = []
        for m in range(0, multiple - 1):
            regions.append([m * int(total_len // multiple), (m + 1) * int(total_len // multiple)])
        regions.append([(multiple - 1) * int(total_len // multiple), total_len])
        p = Pool(multiple)
        temp_process = []
        for i in range(multiple):
            subpopulation=[]
            for index in range(regions[i][0],regions[i][1]):
                gene=population[index][0]
                subpopulation.append([gene[:],0])
            temp_process.append(p.apply_async(sub_shrink, args=(subpopulation,pk_target,winhowmany)))
        p.close()
        p.join()
        population=[]
        for m in temp_process:
            res_process = m.get()
            population+=res_process


    population.sort(key=lambda x: x[1], reverse=1)  # large to small score

    # filter by size
    n = len(population)
    while n > limitsize:
        population.pop() # population the small ones
        n -= 1
    # reset score to 0
    for i in population:
        i[1] = 0
    # checked 10/11/2020
    return population

def mutation(genes, mutated_sites_number, mutation_possiblity_for_single):  # 1 0.15
    # inplace change
    # need to mutation for each candidate
    for _ in range(mutated_sites_number):
        if random.random() < mutation_possiblity_for_single:
            select_position_mutation = [random.randint(0, 49) for m in
                                        range(1)]  # which contain the possition 49
            for i in select_position_mutation:
                genes[i] = random.randint(0, 3)


def record(which_generation, candidates, append='', print_score=0):
    if print_score != 0:
        with open(str(which_generation) + append + '.txt', 'w') as f:
            for i in candidates:
                f.write(''.join([str(x) for x in i[0]]) + ' score=' + str(i[1]) + '\n')
    else:
        with open(str(which_generation) + append + '.txt', 'w') as f:
            for i in candidates:
                f.write(''.join([str(x) for x in i[0]]) + '\n')
