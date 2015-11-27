__author__ = 'omrim'


'''
this file is the store class here we maintain all worker list and extra ifo about workers
'''

class ShopEmployee:
    '''
   details about the employee: name, employee_id, phone, experience, positions
   will hold the experience and positions in the store class
   '''
    def __init__(self, name, employee_id, legal_positions=[], phone=None, experience=0):
        self.name = name
        self.employee_id = employee_id
        self.phone = phone
        self.experience = experience
        self.poss = legal_positions
        # for p in legal_positions:
        #     self.poss.append(p)
        self.assigned = [0,0,0,0,0,0,0]


    def assign(self, day):
        self.assigned[day] = 1

    def set_availability(self, shifts):
        self.available_on = shifts

    def add_position(self, pos):
        self.poss.append(pos)

    def update_eperience(self, new_exp):
        self.experience = new_exp







class Store:
    '''
    holds the details about the store- worker, positions, special conditions
    '''
    def __init__(self, store_name, employee_list):
        self.name = store_name
        self.employees = employee_list

