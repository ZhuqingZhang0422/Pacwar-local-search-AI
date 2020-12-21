import multiprocessing
import _PyPacwar
import numpy
import random
import sys
import os
from collections import defaultdict
import util_xw as util
import threading  # multiple thread
from multiprocessing import Pool,Manager
import copy
# GA design
# Contributor XW



class GA():
    def __init__(self, initialparent, ancient=None, sites=None):
        if ancient is None:
            ancient = [[1] * 50, [3] * 50]
        if sites is None:
            sites = [[0, 4], [4, 20], [20, 23], [23, 26], [26, 38], [38, 50]]
        self.start=[]
        for i in initialparent:
            if i not in self.start:
                self.start.append(i)

        # which is the initial father list of candidiates the candidate should be in a list [[,,]]
        # unique start
        
        self.current_population = [[i, 0] for i in self.start]  # i is the list# [sequence, score]
        self.sites = sites
        self.last_generation=ancient  #no score[genes]
        self.last_chamption = ancient

    #def GA_multipleprocess(self,function,arguments_list,number_of_process):
        #p=Pool(number_of_process)
        #for i in range(number_of_process):
            #p.apply_async(function,args=arguments_list[i])
        #p.close()
        #p.join()


    def fitness(self, multiple):  # take the longest time now
        # take the current population and then combat between the generation and return the best
        if multiple == 1:
            for index_i in range(len(self.current_population)):
                # i=self.current_population[index_i][0]
                for index_j in range(index_i + 1, len(self.current_population)):
                    # j=self.current_population[index_j][0]

                    self.score_function(index_i, index_j)
        else:  # multiple process
            total_len = len(self.current_population)
            temp=copy.deepcopy(self.current_population)
            # reset current_population
            for i in self.current_population:
                i[1]=0 # score reset to 0

            regions=[]
            for m in range(0,multiple-1):
                regions.append([m*int(total_len // multiple),(m+1)*int(total_len // multiple)])
            regions.append([(multiple-1)*int(total_len // multiple),total_len])
            p = Pool(multiple)
            temp_process=[]
            for i in range(multiple):
                temp_process.append(p.apply_async(self.subfitness, args=(i,regions[i],temp)))

            p.close()
            p.join()
            for i in temp_process:
                res_process=i.get()
                for ii in range(len(self.current_population)):
                    self.current_population[ii][1] += res_process[ii][1]

            ##self.GA_multipleprocess(function=self.subfitness,arguments=(regions,),number_of_process=multiple)

    def subfitness(self, core,index_i_position,current_population):
        print('core',str(core),'is working')

        for index_i in range(index_i_position[0], index_i_position[1]):
            for index_j in range(index_i + 1, len(current_population)):
                #    j=self.current_population[index_j][0]
                i=current_population[index_i][0]
                j=current_population[index_j][0]
                if i != j:
                    result_i, result_j = util.outcome_of_duel(i, j)
                    # print(result_i)
                    # print(result_j)
                    current_population[index_i][1] += result_i
                    current_population[index_j][1] += result_j
        return current_population # return to the queue


    def score_function(self, index_i, index_j):  # single process
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
        # inplace
        self.current_population.sort(key=lambda x: x[1], reverse=1)  # from large to small
        while len(self.current_population) > n:
            self.current_population.pop()

    def sub_generate(self,core,index_i_position,current_population,sites,combination_possibility,mutation_record_times,mutated_sites_number,mutation_possiblility_for_single,subling_limit):
        print('core',str(core),'is working')
        # portion cross with all
        res = []
        for index_i in range(index_i_position[0], index_i_position[1]):
            i=current_population[index_i]
            for j in current_population:
                batchgeneration = []
                if i != j:  # avoid self cross over
                    # child generation
                    children = util.crossover(i[0], j[0], combination_possibility, sites)  # unique child
                    for child in children:
                        # mutation + add to the children instead of replacing
                        temp=child[:]
                        if [temp, 0] not in batchgeneration:
                            batchgeneration.append([temp, 0])
                        for _ in range(mutation_record_times):
                            temp2=child[:]
                            util.mutation(temp2, mutated_sites_number, mutation_possiblility_for_single)
                            # shrink the size of the child based on parents
                            if [temp2, 0] not in batchgeneration:
                                batchgeneration.append([temp2, 0])
                    # inplace shrink size of children
                #util.shrink_the_size_of_population(batchgeneration, subling_limit, [i[0], j[0]], -1,multiple=1)
                #print('shrink based on parents')
                util.shrink_the_size_of_population(batchgeneration, subling_limit, [i[0], j[0]], -1,multiple=1)
                #print('shirnk based on brothers')
                #util.shrink_the_size_of_population(batchgeneration, subling_limit, [ t[0] for t in batchgeneration], int(len(batchgeneration)*0.9) ,multiple=1)

                res+=batchgeneration
        return res


    def run(self, generation_limit=100, limitsize=10,winrate=1,selecnumber=2,mutation_record_times=1, mutated_sites_number=1, mutation_possiblility_for_single=0.2,subling_limit=2,multiple=4):
        # after initiate the problem execute this run
        current_generation = 0
        combination_possibility = util.calculate_combine_pattern(len(self.sites))
        while generation_limit != 0:
            print('generation' + str(current_generation),' ;length=',str(len(self.current_population)))
            if len(self.current_population)==0:
                break
            if len(self.current_population)>limitsize:
                # shrink
                print('shrinking the size')
                print('based on '+str(len(self.last_generation)))
                self.current_population=util.shrink_the_size_of_population(copy.deepcopy(self.current_population),limitsize,self.last_generation,int(len(self.last_generation)*winrate),multiple)# win all last generation
                print('generation' + str(current_generation),' ;length=',str(len(self.current_population)))

            # before the battle add the last generation's champion

            print('add the last generation champion to current')

            for i in self.last_chamption:
                if [i[:],0] not in self.current_population:
                    self.current_population.append([i[:],0])
            print('battle')


            self.fitness(multiple)  # battle and update score
            util.record(current_generation, self.current_population, append='all', print_score=1)
            # add to the champion list
            with open('champoin_each_generation.txt', 'a') as f: # append
                i= self.current_population[0]
                f.write(''.join([str(x) for x in i[0]]) + '\n')

            print('selection')

            # store the last generation before selection
            # before the selection, restore the current generation as the last generation
            self.last_generation=[]
            for i in self.current_population:
                #i[1]=0 
                self.last_generation.append(i[0][:]) # only genes

            self.selection(selecnumber)  # inplace change of the current generation # based on the battle result

            # after selection add to the champion
            self.last_chamption=[]
            for i in self.current_population:
                self.last_chamption.append(i[0][:]) # only genes

            util.record(current_generation, self.current_population, append='parent', print_score=1)

            # new generation by random crossover
            print('crossover')
            self.next_generation = []
            # change to multiple process
            total_len = len(self.current_population)
            regions = []
            for m in range(0, multiple - 1):
                regions.append([m * int(total_len // multiple), (m + 1) * int(total_len // multiple)])
            regions.append([(multiple - 1) * int(total_len // multiple), total_len])
            #t0 = threading.Thread(target=self.sub_generate, args=(regions[0],combination_possibility,mutated_sites_number,mutation_possiblility_for_single,subling_limit))
            #self.GA_multipleprocess(function=self.sub_generate,arguments=(regions[0],combination_possibility,mutated_sites_number,mutation_possiblility_for_single,subling_limit),number_of_process=multiple)
            p = Pool(multiple)
            temp_process=[]
            for i in range(multiple):
                temp_process.append(p.apply_async(self.sub_generate, args=(i,regions[i],self.current_population,self.sites,combination_possibility,mutation_record_times,mutated_sites_number,mutation_possiblility_for_single,subling_limit)))
            p.close()
            p.join()
            for i in temp_process:
                res_process_ = i.get()
                for mm in res_process_:
                    if mm not in self.next_generation:
                        self.next_generation.append(mm)
            print('crossover done')
            # done
            # self.current_population=next_generation#[(candidate,0)]
            # reset current generation score to 0

            # record as last generation
            # add last generation to current generation
            self.current_population=[]   # control whether combine or not
            for _ in self.next_generation:  # [(candidate,0)]: # combine
                if _ not in self.current_population:
                    self.current_population.append(_)
            # done

            generation_limit -= 1
            current_generation += 1
        # when it break:
        self.fitness(multiple)
        util.record(current_generation, self.current_population, append='all', print_score=1)
        self.selection(selecnumber)
        util.record(current_generation, self.current_population, append='parent', print_score=1)
        util.record(current_generation, self.current_population, append='final', print_score=0)
        return self.current_population


def main():
    ones = [1] * 50
    threes = [3] * 50
    '''
       
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
    '''
    # new verion use I/O
    # read the current folder path
    current_path=os.path.abspath('.')
    print('current path: '+current_path)
    continue_or_not=input('Do you want to continue to creat a folder to save data? 1:Yes 0:No\n')
    if continue_or_not==0:
        # stop
        return
    new_folder_name=input('Please name the new folder name: \n')
    input_data_file=input('Please enter the input file name \n')
    input_data=[ones,threes]
    with open(input_data_file, 'r') as f:
        candidates=f.readlines()
        for candidate in candidates:
            input_data.append([int(i) for i in candidate.strip('\n')])
    #dir = 'testnew'
    os.mkdir(new_folder_name)
    os.chdir(new_folder_name)
    #print(input_data)
    solution = GA(input_data)
    #res=solution.run()
    res = solution.run(generation_limit=3000000,limitsize=300,winrate=0.8, selecnumber=60,subling_limit=6,mutation_record_times=18,mutated_sites_number=9, mutation_possiblility_for_single=0.05, multiple= multiprocessing.cpu_count())
    print(res)

if __name__ == "__main__": main()
