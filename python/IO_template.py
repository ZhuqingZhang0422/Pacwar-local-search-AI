with open('????.txt', 'a') as f:
    for m in [[1]*50]:
        f.write(str(m) + '\n')
with open('Hill_Climbing_iter_1.txt','r') as f:
    candidates=f.readlines()
for i in range(len(candidates)):
    candidates[i]=candidates[i].strip('\n')
for j in    candidates:
    j_=[int(x) for x in j]