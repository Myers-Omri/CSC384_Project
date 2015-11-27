__author__ = 'omrim'

import random
my_list = [1]*3 + [0]
for e in range(10):
    print('w' + str(e) + '=[' , end=''),
    for d in range(1,8):
        print('[', end=''),
        for s in range(0,4):
            # x = random.choice(my_list)
            if random.random() > 0.5:
                print(str(s), end='')
                if s<3:
                    print(',', end='')
        # x = random.choice(my_list)
        # if random.random() > 0.5:
        #     print(str(3) + ']', end='')
        # else:
        print(']', end='')
        if d<7:
            print(',', end='')
    print(']')