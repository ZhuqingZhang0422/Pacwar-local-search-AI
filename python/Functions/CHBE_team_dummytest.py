import _PyPacwar
import numpy
# Example Python module in C for Pacwar
def main():
    res=[]
    threes = [3] * 50
    ones = [1] * 50
    for pp in range(4):
        origin = [1] * 50
        for i in range(50):
            test= origin[:]
            for j in range(4):
                test[i]=j
                (rounds1, c11, c12) = _PyPacwar.battle(test, ones)
                (rounds2, c21, c22) = _PyPacwar.battle(test, threes)
                if (c11>c12):
                    res.append([rounds1,test[:]])
    res.sort()
    print('test gene',res,'\n')
if __name__ == "__main__": main()
