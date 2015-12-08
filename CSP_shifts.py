__author__ = 'omrim'

from cspbase import Variable, Constraint, CSP, BT
from itertools import product
from propagators import  *

issues_list = []

def create_var_mat(list, n):
    new_var_mat = []

    if len(list) == n:
        return [list]
    for d in range(7):
        day_list = []
        for w in range(n):
            day_list.append(list[(d + w*7)])
        new_var_mat.append(day_list)
    return new_var_mat




def create_variables_w(csp_obj, availabilities):

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

    var_mat = create_var_mat(var_list, len(availabilities))
    return var_mat


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

def create_sat_tuples(var_list,shift,nWorkers,d):

    var_dom_list = []
    for v in var_list:
        var_dom_list.append(v.domain())

    all_comb = product(*var_dom_list)
    list_all_comb = list(all_comb)
    new_sat_tup = []
    ## here we might wanna check if the comb is good for min/max workers per shift.
    while nWorkers>=1:
        for i,p in enumerate(list_all_comb):
            if is_legale(p,shift,nWorkers):
               new_sat_tup.append(p)
        if new_sat_tup:
            break
        if nWorkers>1:
            issues_list.append('could not find solution for {} workers on shift{} day {} try for {} workers instead'.format(nWorkers,shift,d ,(nWorkers-1)))
        nWorkers -= 1

    if nWorkers == 0:
        issues_list.append('could not find any solution for shift{} day {}'.format(nWorkers,shift,d))
    return tuple(new_sat_tup)

def make_constraints_w(csp_obj, vars_mat, nWorkersMat):
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
            cur_scope = []
            for ed, v in enumerate(el):
                if v.in_cur_domain(s):
                    cur_scope.append(v)

            name = 'S{}D{}'.format(s, d+1)
            new_con = Constraint(name, cur_scope)
            sat_tuples = create_sat_tuples(cur_scope,s,nWorkersMat[d][s-1],d+1)


            new_con.add_satisfying_tuples(sat_tuples)


            constraints_list.append(new_con)
            csp_obj.add_constraint(new_con)

    return constraints_list

def create_variables_d(csp_obj, availabilities, day):

    '''

    :param employees: list of employees that are currently work for the store
    :param availabilities: list of lists. every row is list of shifts that the worker can work in
    :return: list of new vars E1D1, E2D1... EmD1..EnD1
    '''
    var_list = []
    for e, al in enumerate(availabilities):
        name = 'E{}D{}'.format(e, day)
        dom = al[day]
        new_var = Variable(name, dom)
        var_list.append(new_var)
        csp_obj.add_var(new_var)

    # var_mat = create_var_mat(var_list, len(availabilities))
    return var_list



def make_constraints_d(csp_obj, vars_list, nWorkersMat, day):
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

    for s in range(1,4):
        cur_scope = []
        for ed, v in enumerate(vars_list):
            if v.in_cur_domain(s):
                cur_scope.append(v)

        name = 'S{}D{}'.format(s, day+1)
        new_con = Constraint(name, cur_scope)
        sat_tuples = create_sat_tuples(cur_scope,s,nWorkersMat[day][s-1],day+1)
        new_con.add_satisfying_tuples(sat_tuples)
        constraints_list.append(new_con)
        csp_obj.add_constraint(new_con)

    return constraints_list


#input:
# @ employees_availability: list of employees - availability matrix for every one
# @ man_req: for every shift the amount of people needed
# @ special_conditions : matrix 7X3 that special_conditions[d][s] is the num of workers required at day d in shift s.
#

def create_week_model( availabilities,  required_workers_mat=[[1,1,1]]*7 ,store = None ):  #employees_availability, man_req, special_const  ):
    shifts_csp = CSP('skiPass_week')
    shifts_mat = create_variables_w(shifts_csp, availabilities)
    constraints__list = make_constraints_w(shifts_csp,shifts_mat, required_workers_mat)
    return shifts_csp

def create_daily_model( availabilities,  required_workers_mat=[[1,1,1]]*7 ,store = None ):  #employees_availability, man_req, special_const  ):
    csp_list = []
    for d in range(7):
        daily_csp = CSP('skiPass_daily{}'.format(d))
        shifts_list = create_variables_d(daily_csp, availabilities,d)
        constraints__list = make_constraints_d(daily_csp,shifts_list, required_workers_mat,d)
        csp_list.append(daily_csp)

    return csp_list

class BTS:
    def __init__(self, csps):
        self.csp_list = csps
        self.n = len(csps)

    def bt_search(self,propagator):
        sol_list = []
        for c in self.csp_list:
            solver = BT(c)
            solver.bt_search(propagator)
            n_sol_list = [x for x in (c.get_soln()) ]
            sol_list.append(n_sol_list)

        return sol_list




def get_availabilities():
    id0=[[0,1]    ,[0,2,3]  ,[0,1,3]  ,[0,1,3]  ,[0,1,2,3],[0,1,2]  ,[0,1,2,3]]
    id1=[[0,2],[0,1,2,3],[0,1,3]  ,[0,1,2,3],[0,1,2,3],[0,1]    ,[0,1,2,3]]
    id2=[[0,3],[0,1,2,3],[0,1,2,3],[0]      ,[0,1,2]  ,[0,2,3]  ,[1]      ]
    id3=[[0,1]  ,[0,1,2,3],[0,2]    ,[0,1]    ,[0]      ,[0,1,2,3],[0]      ]
    id4=[[0,1,2]  ,[0,1,2,3],[0,1]    ,[0,2]    ,[0,2,3]  ,[0,1,2,3],[0,3]    ]
    id5=[[0,1,2]  ,[0,1,2]  ,[0,1,2,3],[0,1,2,3],[0,2,3]  ,[0,1,2,3],[0]      ]
    # id6=[[0]      ,[0,1,2,3],[0]      ,[0,1,2,3],[0,1,3]  ,[0,1,2,3],[0,1,2,3]]
    # id7=[[0,1,2]  ,[0,2]    ,[0,1,2,3],[0]      ,[0,1,2,3],[0,3]    ,[0,3]    ]
    # id8=[[0,2]    ,[0,1,3]  ,[0]      ,[0,1,2,3],[0,1,2]  ,[0,1,2,3],[0,1,2]  ]
    # id9=[[0,1,2,3],[0,1,2]  ,[0,1,2,3],[0]      ,[0,1,2,3],[0]      ,[0,2,3]  ]
    avails = [id0, id1, id2, id3, id4, id5]#, id6, id7, id8, id9]
    return avails

def print_schedule(sol):
    day_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    sift_list = ['Morning', 'Noon', 'Night']
    row_format = "|{:>22}" * (len(day_list) + 1) + '|'
    cel_format = '|{:>22}'
    print (row_format.format("", *day_list))
    for shift, row in zip(sift_list, sol):
        row_arr = []
        for d in row:
            ws = ''
            for w in d:
                ws += str(w)+','
            row_arr.append(ws)
        print (row_format.format(shift, *row_arr))

def fix_to_print(sols,n):
    if not n == -1:
        sol_mat = create_var_mat(sols,n)
    else:
        sol_mat = sols
    sched_mat = []
    for s in range(1,4):
        shift_row = []
        for i,d in enumerate(sol_mat):
            cell = []
            for w,a in d:
                if a == s:
                    cell.append(w.name)
            shift_row.append(cell)
        sched_mat.append(shift_row)
    return sched_mat

def modify_req_mat(mat, c):
    s = int((c.name)[1])
    d = int((c.name)[3])
    cur_n_workers = mat[d-1][s-1]
    if cur_n_workers == 1:
        return mat, False
    mat[d-1][s-1] -= 1
    return mat, True



def run_solver(propType, trace=False):
    nworkers = 10
    avails = get_availabilities()
    required_workers_mat=[[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,2]]
    # r0 = (required_workers_mat[0])
    # r0[2] = 3
    # r0[1] = 2
    # csp = create_model(avails,required_workers_mat)

    flag = True
    res = False
    while (not res) and flag:
        csp = create_week_model(avails,required_workers_mat)
        print("csp created")
        solver = BT(csp)
        if trace:
            solver.trace_on()
        if propType == 'BT':
            solver.bt_search(prop_BT)
        elif propType == 'FC':
            solver.bt_search(prop_FC)
        elif propType == 'GAC':
            res, cons = solver.bt_search(prop_GAC)
        if not res:
            if cons == None:
                print('finding solution took too long proccess terminated, now lets try BTS')
                return
            c,v = cons
            print("the cons that could not be satisfied is {} and the var is{}".format(c,v))
            required_workers_mat, flag = modify_req_mat(required_workers_mat, c)
            if flag:
                print("try for less workers in {}".format(c))

    if not flag and not res:
        print("couldn't find solution")
    else:
        tmpsoln = csp.get_soln()
        soln = fix_to_print(tmpsoln, len(avails))
        print_schedule(soln)


def test_daily():
    avails = get_availabilities()
    required_workers_mat=[[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,1],[1,1,2]]
    csps = create_daily_model(avails,required_workers_mat)
    solver = BTS(csps)
    tmpsoln = solver.bt_search(prop_GAC)
    soln = fix_to_print(tmpsoln, -1 )
    print_schedule(soln)


if __name__ == '__main__':

    run_solver('GAC', False)
    # print (issues_list)
    test_daily()
    # arr = [[(1,2)]*7]*3
    # print_schedule(arr)






