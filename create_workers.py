__author__ = 'omrim'

import random

def get_the_fucking_workers(n):
    

my_list = [1]*3 + [0]
worker_list = []
for e in range(10):
    worker_list.append(('id' + str(e)))
    print('id' + str(e) + '=[' , end=''),
    for d in range(1,8):
        f=1
        if random.random() > 0.85:
            f=4
        print('[', end=''),
        # first = True
        print(str(0), end='')
        spaces = 0
        for s in range(1,4):
            # x = random.choice(my_list)
            if random.random() > 0.3*f:
                print(',' +str(s), end='')
            else:
                spaces += 2



        # x = random.choice(my_list)
        # if random.random() > 0.5:
        #     print(str(3) + ']', end='')
        # else:
        print(']', end='')
        print(' '*spaces, end='')
        if d<7:
            print(',', end='')
    print(']')
for e in range(10):
    print(('id' + str(e) + ', '), end='')
