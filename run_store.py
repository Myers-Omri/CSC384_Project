__author__ = 'omrim'

from retailer import *
import time
from datetime import datetime,date
def load_shifts():
    id0=[[0,2]    ,[0,1]    ,[0,2]    ,[0]      ,[0,1,2,3],[0,2]    ,[0,3]    ]
    id1=[[0,1,3]  ,[0,1,2,3],[0,3]    ,[0,3]    ,[0,1,2]  ,[0]      ,[0,1,2]  ]
    id2=[[0,1,2,3],[0,2,3]  ,[0,2]    ,[0,1,2,3],[0]      ,[0,1,2]  ,[0,1,2,3]]
    id3=[[0,3]    ,[0,1,2,3],[0]      ,[0,2,3]  ,[0,1,2]  ,[0,1,3]  ,[0,1,2,3]]
    id4=[[0]      ,[0,1,2,3],[0,1,2]  ,[0,2,3]  ,[0,1,2,3],[0,1,2,3],[0,1,2,3]]
    id5=[[0]      ,[0,2,3]  ,[0]      ,[0,1,2]  ,[0]      ,[0,1,3]  ,[0,1,2,3]]
    id6=[[0,1,2]  ,[0,2,3]  ,[0,2,3]  ,[0,2,3]  ,[0,1,2]  ,[0,1,2,3],[0]      ]
    id7=[[0,1,2,3],[0,1,2,3],[0,2,3]  ,[0,1,3]  ,[0,1,3]  ,[0,1,3]  ,[0]      ]
    id8=[[0,2,3]  ,[0,2,3]  ,[0,1,2,3],[0,1,3]  ,[0]      ,[0]      ,[0]      ]
    id9=[[0,3]    ,[0,1,2,3],[0,1,2,3],[0,1,2]  ,[0,2]    ,[0,1,3]  ,[0,1,2,3]]
    return [id0, id1, id2, id3, id4, id5, id6, id7, id8, id9]

def get_nworkers_predict(c_month,c_week_day, forecast):
    from math import ceil
    factor = 1
    if c_month in [12,1,2]:
        factor *=2
    if c_week_day in [5,6,7]:
        factor*=1.5
    if forecast in ['sunny', 'snowy']:
        factor*=1.2
    num_workers = int(ceil(3 * factor))


def get_store_data(store):
    return store.name



if __name__ == '__main__':
    skiPass = Store("skiPass", [])
    al_avails = load_shifts()
    for i,a in enumerate(al_avails):
        new_worker = ShopEmployee('Emp{}'.format(i), '000{}'.format(i))
        skiPass.add_employee(new_worker)
    for j, w in enumerate(skiPass.get_all_employees()):
        w.set_availability(al_avails[j])

    c_date = date.today()
    c_month = c_date.month
    c_week_day = c_date.weekday()
    # date = (datetime.month, datetime.day)
    forecast = 'rainy'
    n_workers = get_nworkers_predict(c_month,c_week_day, forecast)
