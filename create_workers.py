__author__ = 'omrim'

from retailer import ShopEmployee
import random


def get_the_workers(n):
    frequency_list = [1]*3 + [0]
    worker_list = []
    for workers in range(n):

        day_list = []
        for day in range(1,8):

            f=1
            if random.random() > 0.85:
                f=4
            shift_list=[0]
            for shift in range(1,4):

                if random.random() > 0.3*f:
                    shift_list.append(shift)
            day_list.append(shift_list)

        worker_list.append(day_list)

    return worker_list



def create_the_workers(n):
    name_list = ['Barry', 'Omri', 'Ron', 'Dror', 'Maayan', 'David', 'Phil', 'Noa']
    family_list = ['S', 'M', 'L', 'S', 'ML', 'Ai', 'B', 'G', 'D','E','F','H']
    my_list = get_the_workers(n)
    shop_employee_list=[]
    for x, worker in enumerate(my_list):
        my_worker= ShopEmployee(random.choice(name_list)+'.'+family_list[x],'E'+str(x))
        my_worker.set_availability(worker)
        shop_employee_list.append(my_worker)

    return shop_employee_list




if __name__ == '__main__':
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
