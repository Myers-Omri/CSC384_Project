__author__ = 'omrim'

from create_workers import create_the_workers
from retailer import *
import time
from datetime import datetime,date

def get_day_predict(c_month,c_week_day, forecast, n):
    from math import ceil
    factor = 1
    if c_month in [12,1,2]:
        factor *=2
    if c_week_day in [5,6,7]:
        factor*=1.5
    if forecast in ['sunny', 'snowy']:
        factor*=1.2
    if forecast in ['rainy']:
        factor*=0.5
    nn = int(ceil(n/6.0 * factor))
    if nn == 0 or nn==1:
        return 2
    return nn

def total_workers_for(c_month, forecast,n=10, f=1):
    import random
    if f == -1:
        return [[1,2,1],[1,1,3],[2,1,1],[1,1,1],[1,1,1],[1,3,1],[1,5,1]]
    total_pred= []
    for d in range(6):
        f = random.choice(forecast)
        s_pred = get_day_predict(c_month,d,  f, n-3)
        daily_pred = [s_pred-1, s_pred, s_pred-1]
        total_pred.append(daily_pred)

    return total_pred


def create_random_store(name, n_emp, n_workers_table):
    shop_emp_list = create_the_workers(n_emp)
    new_store = Store(name, shop_emp_list,n_workers_table)
    return new_store





if __name__ == '__main__':
    # skiPass = Store("skiPass", [])
    # al_avails = load_shifts()
    # for i,a in enumerate(al_avails):
    #     new_worker = ShopEmployee('Emp{}'.format(i), '000{}'.format(i))
    #     skiPass.add_employee(new_worker)
    # for j, w in enumerate(skiPass.get_all_employees()):
    #     w.set_availability(al_avails[j])

    c_date = date.today()
    c_month = c_date.month
    # c_week_day = c_date.weekday()
    # date = (datetime.month, datetime.day)
    forecast = 'rainy'
    n_workers_table = total_workers_for(c_month, forecast, f=-1)
    print(n_workers_table)
    n_emp = max([sum(s) for s in n_workers_table])
    print(n_emp)

    store = create_random_store('skiPass', n_emp, n_workers_table)


