import _PyPacwar
import numpy
# simple hill climbing
import random
import sys
import os
import util_xw as util
import multiprocessing
from multiprocessing import Pool,Manager

class HC():
    def __init__(self,initial=[[1]*50,[3]*50]):
        self.start=initial

    def next_(self,original): #change one can change every point
        res = []
        for i in range(len(original)):
            nbr = original[:]
            for j in range(4):
                nbr[i] = j

                for benchmark in self.start:
                    #(rounds1, c11, c12) = _PyPacwar.battle(nbr, benchmark)
                    result1, result2 = util.outcome_of_duel(nbr, benchmark)

                if result1>result2:
                    res.append([nbr[:],result1])
        res.sort(reverse=1) # large to small value
        if res==[]:
            return []
        else:
            return res[0][0] #gene


    def evolution_HC(self,iteration_limit, firstgeneration,initial_mutation_sitenumber):
        res=[]
        # choose the training set
        #random_start=[]
        #random_set_length=1
        #for _ in range(random_set_length):
            #random_start.append([random.randint(0,3) for i in range(50)])
        #start=random_start[:][0]
        k=1# generate k child from start
        childs=[]

        while k!=0:
            select_position_mutation=[random.randint(0,49) for i in range(initial_mutation_sitenumber)]
            start = firstgeneration[:]
            for i in  select_position_mutation:
                start[i]=random.randint(0,3)
            childs.append([start,0]) # gene and score
            k-=1

        while iteration_limit!=0:
            nbrnode=self.next_(start) # best after battle

            if nbrnode!=[]:
                start=nbrnode
            else:
                return start

            iteration_limit -= 1
        return start

    def run(self,HC_times=2000,iteration_limit=10,firstgeneration=[1]*50,initial_mutation_sitenumber=5,print_=1,SAVEAS='input_HC.txt'):
        res=[]
        for _ in range(HC_times):
            final=self.evolution_HC(iteration_limit,firstgeneration,initial_mutation_sitenumber)
            result1, result2 = util.outcome_of_duel(final, [1]*50)
            result3, result4 = util.outcome_of_duel(final, [3]*50)
            if result1>result2 and result3>result4: # WIN 1 3
                res.append([final])
                if print_==1:
                    with open(SAVEAS,'a') as f:
                        print(final)
                        f.write(''.join([str(x) for x in final]) + '\n')
        return res


def run_sub(firstgeneration):
    solution = HC()
    solution.run(firstgeneration=firstgeneration)


def main():
    ones = [1] * 50
    threes = [3] * 50

    multiple=multiprocessing.cpu_count()
    p = Pool(multiple)
    temp_process = []
    for i in range(multiple):
        #solution = HC()
        #output_data_file = input('Please enter the output file name \n')
        #solution.run(firstgeneration=ones, SAVEAS=output_data_file)
        if i<multiple//2:
            firstgeneration=ones
        else:
            firstgeneration=threes
        temp_process.append(p.apply_async(run_sub, args=(firstgeneration,)))

    p.close()
    p.join()



if __name__ == "__main__": main()

