# This is a random test set generator
import random
import sys
import os

def regular():
    for pp in range(4):
        origin = [pp] * 50
        for i in range(50):
            test = origin[:]
            for j in range(4):
                test[i] = j
                with open('testset.txt', 'a') as f:
                    f.write(''.join([str(x) for x in test]) + '\n')


def random_generate(num):
    for i in range(num):
        test=[random.randint(0,3) for i in range(50)]

        with open('testset.txt', 'a') as f:
            f.write(''.join([str(x) for x in test]) + '\n')

if __name__ == "__main__":random_generate(15000)#regular()
