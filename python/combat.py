import _PyPacwar
import numpy
# test set
def main():
    # read the input file
    candidates=[]
    with open('dummy.txt','r') as f:
        candidates_temp=f.readlines()
    for i in range(len(candidates_temp)):
        temp1=candidates_temp[i].strip('\n')
        if temp1 not in candidates:
            candidates.append(temp1)
    # read the test set
    with open('testset.txt', 'r') as f:
        test_warrior = f.readlines()
    for i in range(len(test_warrior)):
        test_warrior[i] =test_warrior[i].strip('\n')
    test_warrior=test_warrior[0:10000]
    # battle now!!
    battle_res=[]
    for i in candidates:
        score=0
        candidates_=[int(x) for x in i]
        wintimes=0
        for j in test_warrior:
            (rounds, c1, c2) = _PyPacwar.battle(candidates_, [int(x) for x in j])
            if c1>c2: # win!!
                wintimes+=1
                if rounds <50:
                    score+=3
                elif rounds <200:
                    score+=2
                else:
                    score+=1
        battle_res.append([score,wintimes,i])
    battle_res.sort(reverse=1)
    with open('battleres.txt','a') as f:
        for m in battle_res:
            f.write(str(m)+'\n')
    # ranking of the candidate use the test set
if __name__ == "__main__": main()
