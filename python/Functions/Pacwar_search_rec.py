import util
import _PyPacwar
import numpy
from heapq import *
class PacMite:
    '''
    Record PacMite gene and keep track of its value campared with the reference mite
    '''
    def __init__(self,gene):
        self.gene = gene
        self.value_factor = self.cal_value_fector(gene)

    def __lt__(self,other):
        return self.val_factor < self.val_factor

    def cal_value_fector(self,gene):
        gene = gene.copy()
        Comparison_1 = [1] * 50
        Comparison_2 = [3] * 50
        (rounds_1, c1_1, c1_2) = _PyPacwar.battle(gene, Comparison_1)
        (rounds_2, c2_1, c2_2) = _PyPacwar.battle(gene, Comparison_2)
        return (rounds_1 + rounds_2,c1_1 - c1_2,c2_1 - c2_2)


def main():
    minheap = []
    init_Gene = [1] * 50
    prev_gene = PacMite(init_Gene)
    cur_gene = PacMite(init_Gene)
    print(prev_gene.gene)
    index = 1
    while True:
        prev_gene = cur_gene
        for i in range(50):
            minheap = []
            Gene = cur_gene.gene
            #print(Gene)
            for j in range(4):
                Gene[i] = j
                Gene = Gene.copy()
                test_gene = PacMite(Gene)
                values = test_gene.value_factor
                if values[1] > 0 and values[2] > 0:
                    heappush(minheap,(Gene,values))
                    print(Gene)
        if minheap != []:
            cur_gene = PacMite(minheap[0][0])
        elif cur_gene.value_factor[0] > prev_gene.value_factor[0] or index>2:
            break
        else:
            index += 1
            print("Index Number:",index,cur_gene.gene,cur_gene.value_factor,"/n")
    '''
    Comparison_1 = [1] * 50
    Comparison_2 = [3] * 50
    res = [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
           1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    print(_PyPacwar.battle(res, Comparison_1), _PyPacwar.battle(res, Comparison_2))
    '''
if __name__ == "__main__": main()


