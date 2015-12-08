__author__ = 'omrim'


'''
this file is the store class here we maintain all worker list and extra ifo about workers
'''

class ShopEmployee:
    '''
   details about the employee: name, employee_id, phone, experience, positions
   will hold the experience and positions in the store class
   '''
    def __init__(self, name, employee_id, phone=None, experience=True):
        self.name = name
        self.id = employee_id
        self.phone = phone
        self.experience = experience
        self.available = []
        # for p in legal_positions:
        #     self.poss.append(p)
        self.assigned = [0,0,0,0,0,0,0]



    def assign(self, day):
        self.assigned[day] = 1

    def set_availability(self, shifts):
        for s in shifts:
            self.available.append(s)

    def add_position(self, pos):
        self.available.append(pos)

    def update_experience(self, new_exp):
        self.experience = new_exp







class Store:
    '''
    holds the details about the store- worker, positions, special conditions
    '''
    def __init__(self, store_name, employee_list, workers_table=[[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1]]):
        self.name = store_name
        self.employees = employee_list
        self.n_workers_table = workers_table

    def add_employee(self, emp):
        for e in emp:
            self.employees.append(e)

    def update_nworkers(self, u_tuple):
        d,s,n = u_tuple
        self.n_workers_table[d][s] = n

    def get_all_employees(self):
        return self.employees

    def get_emp_by_id(self, id):
        for i in self.employees:
            if i.id == id:
                return i

    def get_availabilities(self):
        avail_list = []
        for e in self.employees:
            avail_list.append(e.available)
        return avail_list

    def nume_emp(self):
        return len(self.employees)



