import _PyPacwar
import numpy
import random
import sys
import os

class search:

    def __it__(self):

    def next(original): #change one
        res = []
        for i in range(len(original)):
            nbr = original[:]
            for j in range(4):
                nbr[i] = j
                (rounds1, c11, c12) = _PyPacwar.battle(nbr, ones)
                (rounds2, c21, c22) = _PyPacwar.battle(nbr, threes)
                if c11 > c12 and c21 > c22:
                    res.append([rounds1+rounds2, c11, c12, nbr[:]])
        res.sort()
        if res==[]:
            return []
        else:
            return res[0]
    #print(next([1]*50))

    def HC(iteration_limit,firstgeneration,initial_mutation_sitenumber):
        res=[]
        # choose the training set
        #random_start=[]
        #random_set_length=1
        #for _ in range(random_set_length):
            #random_start.append([random.randint(0,3) for i in range(50)])
        #start=random_start[:][0]
        k=500
        while k!=0:
            select_position_mutation=[random.randint(0,49) for i in range(initial_mutation_sitenumber)]

            for i in  select_position_mutation:
                start=firstgeneration[:]
                start[i]=random.randint(0,3)

            (rounds1, c11, c12) = _PyPacwar.battle(start, ones)
            (rounds2, c21, c22) = _PyPacwar.battle(start, threes)
            if c11>c12 and c21>c22:
                break
            k-=1
        currentrounds=rounds1+rounds2

        while iteration_limit!=0:
            nbrnode=next(start) # best after battle

            if nbrnode==[]:
                return start
            else:
                next_gene=nbrnode[3]
                next_rounds=nbrnode[0]
                if next_gene == start:
                    return start
                else:
                    if currentrounds <next_rounds:
                        return start
                    else:
                        start=next_gene[:]
            iteration_limit -= 1
        return next_gene

    iteration_limit=50
    HC_times=10
    firstgeneration=[1]*50
    for _ in range(HC_times):
        final=HC(iteration_limit=iteration_limit,firstgeneration=firstgeneration,initial_mutation_sitenumber=10)
        #print(final)
        with open('dummy.txt','a') as f:
            if final!=firstgeneration:
                print(final)
                f.write(''.join([str(x) for x in final])+'\n')