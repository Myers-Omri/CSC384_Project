__author__ = 'omrim'

from cspbase import Variable, Constraint, CSP
from itertools import product

def create_variables(csp_obj, availabilities):

    '''

    :param employees: list of employees that are currently work for the store
    :param availabilities: list of lists. every row is list of shifts that the worker can work in
    :return: list of new vars E1D1, E1D2... E2D1..EnD7
    '''
    var_list = []
    for e, al in enumerate(availabilities):
        for d, sl in enumerate(al):
            name = 'E{}D{}'.format(e, d)
            dom = sl
            new_var = Variable(name, dom)
            var_list.append(new_var)
            csp_obj.add_var(new_var)
    return var_list


def is_legale(permute, shift, nWorkers):

    tot_workers = 0
    for sw in permute:
        if sw == shift:
            tot_workers += 1
        if tot_workers > nWorkers: ##maybe enable >=nWorkers
            return False
    if tot_workers < nWorkers:
        return False

    return True

def create_sat_tuples(var_list,shift,nWorkers):
    var_dom_list = []
    for v in var_list:
        var_dom_list.append(v.domain())

    all_comb = product(*var_dom_list)
    list_all_comb = list(all_comb)
    ## here we might wanna check if the comb is good for min/max workers per shift.
    for i,p in enumerate(list_all_comb):
        if not is_legale(p,shift,nWorkers):
            list_all_comb.pop(i)
    return tuple(list_all_comb)

def make_constraints(csp_obj, vars_mat, nWorkersList):
    '''

    :param csp_obj:
    :param vars_mat: row of all employees by day-
                        E1D1, E2D1, E3D1, E4D1, .. EnD1
                        E1D2, E2D2, E3D2, E4D2, ..
                        ...
                        ...
                        E1D7.......................EnD7
    :param: nWorkersList a matrix of the num of workers for each shift.
    :return: constraint list
    '''

    constraints_list = []
    for d, el in enumerate(vars_mat):
        for s in range(1,4):
            cur_con_var_list = []
            for ed, v in enumerate(el):
                if v.in_cur_domain(s):
                    cur_con_var_list.append(v)
            name = 'S{}D{}'.format(s, d)
            new_con = Constraint(name, cur_con_var_list)
            sat_tuples = create_sat_tuples(cur_con_var_list,s,nWorkersList[d][s])
            new_con.add_satisfying_tuples(sat_tuples)
            constraints_list.append(new_con)
            csp_obj.add_constraint(new_con)

    return constraints_list












#input:
# @ employees_availability: list of employees - availability matrix for every one
# @ man_req: for every shift the amount of people needed
# @ special_const
#

def create_model(store, availabilities, special_conditions ):  #employees_availability, man_req, special_const  ):

    shifts = create_variables(store.employees, availabilities)
    shifts_csp = CSP






