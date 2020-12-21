import util
import _PyPacwar
import numpy
import combat
from heapq import *
from collections import defaultdict

class PacMite:
    '''
    Record PacMite gene and keep track of its value campared with the reference mite
    '''

    def __init__(self,gene):
        self.gene = gene
        self.ref_value= self.ref_value()
        self.ref_record = []

    def __lt__(self,other):
        return self.val_factor < self.val_factor

    def ref_value(self):
        '''
        :param gene:
        :return value factor of gene combat
        '''
        gene = self.gene
        Comparison_1 = [1] * 50
        Comparison_2 = [3] * 50
        (rounds_1, c1_1, c1_2) = _PyPacwar.battle(gene, Comparison_1)
        (rounds_2, c2_1, c2_2) = _PyPacwar.battle(gene, Comparison_2)
        return rounds_1 + rounds_2,c1_1 - c1_2,c2_1 - c2_2

    def rec_successor(self,capacity):
        record = self.ref_record
        gene = self.gene
        value = self.ref_value
        if gene not in record:
            heappush(record,(value,gene))
        while len(record) > capacity:
            heappop(record)

    def save_gene(self):
        with open('Candidate.txt','a') as f:
            gene_name = ''.join([str(x) for x in self.gene])
            gene_value = self.ref_value
            f.write('Gene Name: *'+ gene_name +' *Ref_score* '+ str(gene_value) +'\n')

    def reorder_candidate(self):
        minheap = []
        with open('Candidate.txt','r') as inp, open('Rank of candidate.txt','w') as out:
            for line in inp:
                if line.strip():
                    continue
            #line = line.replace('[', '')
            #line = line.replace(']', '')
            #line_list = line.split('*')
            #gene_name = line_list[1]
            #value_factor = line_list[3].split(',')[0]
            #heappush([gene_name,value_factor])
            print(line,'/n')

def main():
    gene = [1]*50
    a = PacMite(gene)
    a.save_gene()
    a.reorder_candidate()

if __name__ == "__main__": main()


