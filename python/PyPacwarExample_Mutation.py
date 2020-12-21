import _PyPacwar
import numpy
from heapq import *
# Example Python module in C for Pacwar
def main():
	Comparison_1 = [1] * 50
	Comparison_2 = [3] * 50
	prev = ([1] * 50,500)
	pos = [0, 1, 2, 3]
	cur =  ([1]*50, 500)
	while prev[1] >= cur[1]:
		i = 1
		res = []
		cur = prev
		for i in range (50):
			Gene = cur[0].copy()
			for j in pos:
				Gene[i] = j
				Gene.copy()
				(rounds_1, c1_1, c1_2) = _PyPacwar.battle(Gene, Comparison_1)
				(rounds_2, c2_1, c2_2) = _PyPacwar.battle(Gene, Comparison_2)
				if int(c1_1) - int(c1_2) > 0 and c2_1 - c2_2 >0:
					a = _PyPacwar.battle(Gene, Comparison_1)
					b = _PyPacwar.battle(Gene, Comparison_2)
					heappush(res,(a[0]+b[0],a[0],b[0],Gene))
		cur = (res[0][0],res[0][3])
		print ('Iteration Number:',i,res[0],'/n')

	'''
	test =  [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	Comparison_1 = [1] * 50
	Comparison_2 = [3] * 50
	print(_PyPacwar.battle(test, Comparison_1),_PyPacwar.battle(test, Comparison_2),test)
	#print(res,len(res))
	print(res[0])
	#print ("Example Python module in C for Pacwar")
	#print ("all ones versus all threes ...")
	#(rounds,c1,c2) = _PyPacwar.battle(Test_Gene_1, Test_Gene_2)
	#print ("Number of rounds:", rounds )
	#print ("Test_Gene_1 PAC-mites remaining:", c1)
	#print ("Test_Gene_2 PAC-mites remaining:", c2)
	'''


if __name__ == "__main__": main()
