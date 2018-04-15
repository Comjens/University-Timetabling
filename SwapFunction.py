def swap(sol, timetable, Obj, Courses_max, total_timeslots, rooms_max, F_ct, chi, data, Iter, Placement, AllowDecrease):
    import random
    from FeasibilityCheck import Feasibility_Check
    from itertools import product
    import copy
    from OptimValue import Set_obj
    
    'Loop until a successful swap can be achieved'
    Successful = False
    Optimum = False

    'Define the initial entries'
    c1list = list(range(0, Courses_max))

    QL = data.qua.QL
    IL = data.qua.IL
    # print("QL = ", QL)
    # , "\nIL = ", IL)

    "Update the quarantine list"
    k = len(IL) - 1
    while k >= 0:
        if IL[k] == Iter:
            data.qua.RemQua(QL[k], IL[k])
        else:
            del c1list[c1list.index(QL[k])]                        
        k = k - 1

    InitWorkingDays = copy.deepcopy(data.Workingdays_c)
    WorkingDays = []

    for i, j in enumerate(InitWorkingDays):
        if j >= 1 and (i in c1list):
            WorkingDays.append(i)
            del c1list[c1list.index(i)]

    MergedList = c1list + WorkingDays

    # print("c1list = ", c1list)
    #print("WorkingDays = ", WorkingDays)
       
    while Successful == False:

        "If no moves exist that would allow the objective to increase for any c1, we're at an optimum"
        if len(MergedList) == 0:
            Optimum = True
            break

        "Choose a c1 at random from the candidate list and delete the course we're currently working with from the list of available c1 courses"
        if 1 - Placement <= data.params['Epsilon']:
            c1 = MergedList[random.randint(0, len(MergedList) - 1)]
            del MergedList[MergedList.index(c1)]

        elif 1 - Placement > data.params['Epsilon'] and len(WorkingDays) != 0:
            c1 = WorkingDays[random.randint(0, len(WorkingDays) - 1)]
            del WorkingDays[WorkingDays.index(c1)]
            MergedList = c1list + WorkingDays

        else:
            c1 = c1list[random.randint(0, len(c1list) - 1)]
            del c1list[c1list.index(c1)]
            MergedList = c1list + WorkingDays

        c1_pop_list = []
        c1_np_list = []

        for i, j in enumerate(sol[c1]):
            if j != (None, None):
                c1_pop_list.append(i)
            else:
                c1_np_list.append(i)

        "Loop through all possible c1 lectures before opting to select a new c1"
        while (len(c1_pop_list) != 0 or len(c1_np_list) != 0) and Successful == False:
            if 1 - Placement <= data.params['Epsilon']:
                if len(c1_np_list) != 0:
                    "If we happen to test a (None, None) c1 lecture, there would be no point in testing any other (None, None) c1 lectures"
                    c1_index = c1_np_list[0]
                    c1_np_list = []

                else:
                    "Populating the matrix is of the utmost importance"
                    data.qua.AddQua(c1, Iter + data.params['Gamma'])
                    # print("Quarantined84 c1 = ", c1)
                    break
            else:
                if len(c1_pop_list) != 0:
                    "Cycle through all populated entries first"
                    c1_pop_index = random.randint(0, len(c1_pop_list) - 1)
                    c1_index = c1_pop_list[c1_pop_index]
                    del c1_pop_list[c1_pop_index]

                elif len(c1_np_list) != 0:
                    "If we happen to test a (None, None) c1 lecture, there would be no point in testing any other (None, None) c1 lectures"
                    c1_index = c1_np_list[0]
                    c1_np_list = []
                else:
                    "If both lists are empty, we've already cycled through all possibilities"
                    data.qua.AddQua(c1, Iter + data.params['Gamma'])
                    # print("Quarantined c1100 = ", c1)
                    break

            t1, r1 = sol[c1][c1_index]

            'Determine the c1 status'
            if sol[c1][c1_index] == (None, None):
                c1Null = True
            else:
                c1Null = False

            'Assemble the list of potential courses to swap with'
            c2list = list(range(0, Courses_max))

            "Delete c1 from the list of courses we can swap with, so that we don't swap c1 with itself"
            del c2list[c2list.index(c1)]

            # for i in QL:
            # if i in c2list:
            # del c2list[c2list.index(i)]

            'Loop until a successful swap with c2 can be achieved, otherwise choose a new c1 lecture'
            while Successful == False:
                'If the list is empty, then there exist no beneficial moves for the c1 lecture, choose a new c1 lecture'
                if len(c2list) == 0:
                    break

                'Choose a course from the list of possible swaps, then remove it to prevent repeat iterations'
                c2_index = random.randint(0, len(c2list) - 1)
                c2 = c2list[c2_index]
                del c2list[c2_index]

                "Determine which dictionary entries are populated, and which aren't, then store these indices"
                CountP = 0
                CountNP = 0
                c2_pop_list = []
                c2_np_list = []

                for i, j in enumerate(sol[c2]):
                    if j != (None, None):
                        c2_pop_list.append(i)
                        CountP = CountP + 1;
                    else:
                        c2_np_list.append(i)
                        CountNP = CountNP + 1;

                while (len(c2_pop_list) != 0 or len(c2_np_list) != 0) and Successful != True:
                    'Call the dictionary for c2 and randomly select the sub-dict to use from the populated entries'
                    if len(c2_pop_list) != 0:
                        pop_index = random.randint(0, len(c2_pop_list) - 1)
                        c2_index = c2_pop_list[pop_index]
                        t2, r2 = sol[c2][c2_index]

                        c2Null = False

                        del c2_pop_list[pop_index];

                    elif len(c2_pop_list) == 0 and len(c2_np_list) != 0:
                        '''If both sol[c1_index] and sol[c2_index] are null entries in sol, find a new c2_index.
                        We iterate through the populated entries first, so there are no other populated options'''
                        if c1Null:
                            break

                        "If we've already tried to drop c1 and it didn't work, there's no point in trying again"
                        if len(c2_np_list) != CountNP:
                            break

                        c2Null = True

                        'Call the dictionary for c2 and randomly select the sub-dict to use from the non-populated entries'
                        np_index = random.randint(0, len(c2_np_list) - 1)
                        c2_index = c2_np_list[np_index]

                        del c2_np_list[np_index]

                    else:
                        'If both lists are empty, then none of the swaps with c2 are feasible'
                        break

                    # Cases
                    # 1) Both sol[c1_index] and sol[c2_index] are scheduled --> SWAP
                    # 2) Only sol[c2_index] is scheduled --> ADD
                    # 3) Only sol[c1_index] is scheduled --> DROP
                    # 4) Neither are scheduled --> not permitted, handled earlier in the code

                    'Break down the process by CASE'
                    if c1Null == False and c2Null == False:
                        'CASE 1: Both sol[c1_index] and sol[c2_index] entries are non-null --> swap'

                        'If all three layers of checks are successful, implement the change, else choose new instance'
                        'Continue the evaluation only if the swap is not on the tabu list'
                        if not data.tab.CheckTab((c1, t2, r2)) and not data.tab.CheckTab((c2, t1, r1)):

                            'Create the provisional timetable to evaluate the new objective'
                            ProvTimetable = copy.deepcopy(timetable)
                            ProvTimetable[c1, t1, r1] = 0
                            ProvTimetable[c2, t2, r2] = 0

                            'Check if the replacements are feasible for their destinations'
                            if Feasibility_Check(c2, t1, r1, ProvTimetable, Courses_max, F_ct, data) \
                                    and Feasibility_Check(c1, t2, r2, ProvTimetable, Courses_max, F_ct, data):

                                ProvTimetable[c1, t2, r2] = 1
                                ProvTimetable[c2, t1, r1] = 1

                                'Check if the objective is better'
                                ProvObj = Set_obj(data, ProvTimetable)
                                if ProvObj < Obj:
                                    Successful = True
                                    # print("CASE 1: Swap\nNew obj = ", ProvObj)
                                    # print("Previous obj = ", Obj)
                                    data.qua.AddQua(c1, Iter + data.params['Sigma'])
                                    data.qua.AddQua(c2, Iter + data.params['Sigma'])
                                    break
                                else:
                                    if AllowDecrease:
                                        Successful = True
                                        # print("CASE 1: Swap (NEGATIVE)\nNew obj = ", ProvObj)
                                        # print("Previous obj = ", Obj)
                                        data.qua.AddQua(c1, Iter + data.params['Sigma'])
                                        data.qua.AddQua(c2, Iter + data.params['Sigma'])
                                        break
                    elif c1Null == True and c2Null == False:
                        'CASE 2: sol[c1_index] is unscheduled and sol[c2_index] is non-null --> add sol[c1_index] at random'

                        'We need to iterate between all possible combinations of t2, r2'
                        Possibilities = list(product(list(range(total_timeslots)), list(range(rooms_max))))

                        'We iterate while there are still potential replacements in the list, break on a success'
                        while len(Possibilities) != 0 and Successful != True:
                            'Initialize the t2 and r2 to be used for the current iteration'
                            poss_index = random.randint(0, len(Possibilities) - 1)
                            t2, r2 = Possibilities[poss_index]
                            del Possibilities[poss_index]

                            'If all three layers of checks are successful, implement the change, else reiterate'
                            'Continue the evaluation only if the move is not on the tabu list'
                            if not data.tab.CheckTab((c1, t2, r2)):

                                'Check if the replacements are feasible for their destinations'
                                if Feasibility_Check(c1, t2, r2, timetable, Courses_max, F_ct, data):
                                    ProvTimetable = copy.deepcopy(timetable)
                                    ProvTimetable[c1, t2, r2] = 1

                                    'Check if the objective is better'
                                    ProvObj = Set_obj(data, ProvTimetable)
                                    if ProvObj < Obj:
                                        Successful = True
                                        # print("CASE 2: Add\nNew obj = ", ProvObj)
                                        # print("Previous obj = ", Obj)
                                        data.qua.AddQua(c1, Iter + data.params['Sigma'])
                                        break
                                    else:
                                        if AllowDecrease:
                                            Successful = True
                                            # print("CASE 2: Add (NEGATIVE)\nNew obj = ", ProvObj)
                                            # print("Previous obj = ", Obj)
                                            data.qua.AddQua(c1, Iter + data.params['Sigma'])
                                            break
                    else:
                        'CASE 3: sol[c1_index] is non-null and sol[c2_index] is unscheduled --> drop c1'

                        'If all two layers of checks are successful, implement the change, else choose new c2_index'
                        # 'Continue the evaluation only if the move is not on the tabu list'
                        # if CheckTab[c1, t2, r2]:

                        'Create the provisional timetable to evaluate the new objective'
                        ProvTimetable = copy.deepcopy(timetable)
                        ProvTimetable[c1, t1, r1] = 0

                        ProvObj = Set_obj(data, ProvTimetable)

                        'Check if the objective is better'
                        if ProvObj < Obj:
                            Successful = True
                            # print("CASE 3: Drop\nNew obj = ", ProvObj)
                            # print("Previous obj = ", Obj)
                            break
                        else:
                            if AllowDecrease:
                                Successful = True
                                # print("CASE 3: Drop (NEGATIVE)\nNew obj = ", ProvObj)
                                # print("Previous obj = ", Obj)
                                # data.qua.AddQua(c1, Iter + Sigma)
                                break
                        
    #Cases
    #1) Both sol_entry and c1 are scheduled --> SWAP
    #2) Only sol_entry is scheduled --> ADD
    #3) Only c1 scheduled --> DROP
    #4) Neither are scheduled --> not permitted, handled earlier in the code
    if Successful == True:
        # print(" (c1, t1, r1) = ", c1, ",", t1, ",", r1, "\n", "(c2, t2, r2) = ", c2, ",", t2, \
        #",", r2)
    
        'CASE 1: Both sol[c1_index] and sol[c2_index] entries are non-null --> swap'
        if not c1Null and not c2Null:
            sol[c1][c1_index] = [t2, r2]
            sol[c2][c2_index] = [t1, r1]
             
            timetable[c1, t1, r1] = 0
            timetable[c2, t2, r2] = 0
            timetable[c1, t2, r2] = 1
            timetable[c2, t1, r1] = 1
            
            data.tab.AddTab((c1, t1, r1))
            data.tab.AddTab((c2, t2, r2))
            
        'CASE 2: sol[c1_index] is unscheduled and sol[c2_index] is non-null --> add c1 at random'
        if c1Null and not c2Null:
            sol[c1][c1_index] = [t2, r2]
            timetable[c1, t2, r2] = 1
            
            data.tab.AddTab((c1, None, None))
        
        'CASE 3: sol[c1_index] is non-null and sol[c2_index] is unscheduled --> drop c1'
        if not c1Null and c2Null:
            sol[c1][c1_index] = [None,None]  
            timetable[c1, t1, r1] = 0
            
            data.tab.AddTab((c1, t1, r1))
    #print("line 322")
    return Optimum

# ciao = swap(data.sol, data.timetable, CurrentObj, data.Courses_max, data.total_timeslots, data.rooms_max, data.F_ct, data.Chi_cc,data)
