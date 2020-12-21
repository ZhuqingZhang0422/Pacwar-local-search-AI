import _PyPacwar
import numpy
import os

import util_xw
# test set
def main():
    # read the input file
    candidates=[]
    #os.chdir(r'testnew')


    with open('ubuntugjh_GAV3_120_09_12_18_6_6_CHampoin_each_generation.txt','r') as f:
        candidates_temp=f.readlines()
    for i in range(len(candidates_temp)):
        temp1=candidates_temp[i].strip('\n')
        if temp1 not in candidates:
            candidates.append(temp1)
    # read the test set
    test_warrior=[[1]*50,[3]*50]
    # battle now!!
    battle_res=[]
    for i in candidates:
        score=0
        survive=0
        candidates_=[int(x) for x in i]
        for j in test_warrior:
            r1,r2= util_xw.outcome_of_duel(candidates_, [int(x) for x in j])
            if r1>r2: # win!!
                score+=r1
                
        

        battle_res.append([score,i])
    battle_res.sort()
    with open('battleres13_ubuntugjh_GAV3_120_09_12_18_6_6_CHampoin_each_generation.txt','a') as f:
        for m in battle_res:
            f.write(str(m)+'\n')
    # ranking of the candidate use the test set
if __name__ == "__main__": main()
