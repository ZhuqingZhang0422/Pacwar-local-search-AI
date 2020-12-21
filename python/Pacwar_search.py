import util
import _PyPacwar
import numpy
import combat
from heapq import *

class PacMite:
    '''
    Record PacMite gene and keep track of its value campared with the reference mite
    '''

    def __init__(self,gene):
        self.gene = gene
        self.value_factor = self.cal_value_factor(gene)
        self.

    def __lt__(self,other):
        return self.val_factor < self.val_factor

    def ref_value(self,gene):
        '''
        :param gene:
        :return value factor of gene combat
        '''
        gene = gene.copy()
        Comparison_1 = [1] * 50
        Comparison_2 = [3] * 50
        (rounds_1, c1_1, c1_2) = _PyPacwar.battle(gene, Comparison_1)
        (rounds_2, c2_1, c2_2) = _PyPacwar.battle(gene, Comparison_2)
        return (rounds_1 + rounds_2,c1_1 - c1_2,c2_1 - c2_2)

def main():
    minheap = []
    for i in range(50):
        minheap = []
        Gene = [3]*50
        Gene = Gene.copy()
        for j in range(4):
            Gene = Gene.copy()
            Gene[i] = j
            test_gene = PacMite(Gene)
            values = test_gene.value_factor
            if values[1] > 0 and values[2] > 0 and values[0]<500:
                #print(Gene,values)
                heappush(minheap,(Gene,values))
    print(minheap[0])
    Comparison_1 = [1] * 50
    Comparison_2 = [3] * 50
    res = [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    print(_PyPacwar.battle(res, Comparison_1), _PyPacwar.battle(res, Comparison_2))


if __name__ == "__main__": main()


