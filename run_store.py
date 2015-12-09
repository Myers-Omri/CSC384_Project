__author__ = 'omrim'

from create_workers import create_the_workers
from retailer import *
import time
from datetime import datetime,date
import random
import CSP_shifts
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
        return 1
    return nn

def total_workers_for(c_month, forecast,n=10, f=1):
    import random
    if f == -1:
        return [[1,2,1],[1,1,3],[2,1,1],[1,1,1],[1,1,1],[1,3,1],[1,5,1]]
    total_pred= []
    for d in range(7):
        f = random.choice(forecast)
        s_pred = get_day_predict(c_month,d,  f, n-3)
        m=s_pred
        if s_pred>1: m=s_pred-1
        daily_pred = [m, s_pred, m]
        total_pred.append(daily_pred)

    return total_pred

def create_csv(wekk, dayy, fname):
    import csv

    myfile = open(fname, 'wb')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(['nworkers', 'Time week model', 'time_day_model'])
    labels = zip(wekk, dayy)
    for i, l in enumerate(labels):
        wr.writerow([i+5, l[0], l[1]])

    myfile.close()


def create_random_store(name, n_emp, n_workers_table):
    shop_emp_list = create_the_workers(n_emp)
    new_store = Store(name, shop_emp_list,n_workers_table)
    return new_store





if __name__ == '__main__':
    week_data = []
    day_data = []
    for n_e in range(4,8):
        c_date = date.today()
        c_month = c_date.month
        forecast = ['rainy', 'sunny', 'snowy']
        nw=n_e
        n_workers_table = total_workers_for(c_month, forecast, nw)
        print(n_workers_table)
        n_emp = max([sum(s) for s in n_workers_table])
        print(n_emp)
        store = create_random_store('skiPass', nw, n_workers_table)
        print("the store name is:" + store.name)
        print("workers list:", [e.id for e in store.get_all_employees()])
        print("table of required workers:", store.n_workers_table)
        print("table of availability: ")
        for a in store.get_all_employees():
            print(a.name, "   can work on:",[(d[1:]) for d in a.available])


        w = CSP_shifts.run_solver( 'GAC',store)
        d = CSP_shifts.test_daily(store)
        week_data.append(str(w[0]))
        day_data.append(str(d[0])[:5])
    for i, d in enumerate(zip(week_data,day_data)):
        print(i+4, d[0], d[1])

    #create_csv(['2','2'],day_data,'res_csv_Ai.csv')









    # # skiPass = Store("skiPass", [])
    # # al_avails = load_shifts()
    # # for i,a in enumerate(al_avails):
    # #     new_worker = ShopEmployee('Emp{}'.format(i), '000{}'.format(i))
    # #     skiPass.add_employee(new_worker)
    # # for j, w in enumerate(skiPass.get_all_employees()):
    # #     w.set_availability(al_avails[j])
    #
    # c_date = date.today()
    # c_month = c_date.month
    # # c_week_day = c_date.weekday()
    # # date = (datetime.month, datetime.day)
    # forecast = 'rainy'
    # n_workers_table = total_workers_for(c_month, forecast, f=-1)
    # print(n_workers_table)
    # n_emp = max([sum(s) for s in n_workers_table])
    # print(n_emp)
    #
    # store = create_random_store('skiPass', n_emp, n_workers_table)
    #

