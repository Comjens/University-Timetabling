def swap(sol, timetable, Obj, Courses_max, total_timeslots, rooms_max, F_ct, chi, data, Iter):
    import random
    from FeasibilityCheck import Feasibility_Check
    from itertools import product
    import copy
    from OptimValue import Set_obj   
    
    'Loop until a successful swap can be achieved'
    Successful = False
    Optimum = False
    # parameter that states after how many iterations we can remove a number from the quarantine list
    Gamma = 15
    Sigma = 9
    c1list = list(range(0, Courses_max))
    QL = data.qua.QL
    IL = data.qua.IL
    # print('c1',c1list)
    print(QL, IL)
    k = len(IL) - 1
    while k >= 0:
        if IL[k] == Iter:
            data.qua.RemQua(QL[k], IL[k])
            c1list.append(QL[k])
        else:
            if c1list.__contains__(QL[k]):
                del c1list[c1list.index(QL[k])]
            else:
                print("Was this picked from c2?", QL[k])

        k = k - 1
    # print('updatedListq',QL,'\ni:',IL)
    # print(c1list)
    while Successful == False:
        print('Quarantine list', data.qua.QL)
        "If no moves exist that would allow the objective to increase for any c1, we're at an optimum"
        if len(c1list) == 0:
            Optimum = True
            break
        
        'Define the initial entries'
        c1 = c1list[random.randint(0, len(c1list)-1)]
        c1_index = random.randint(0, len(sol[c1])-1)
        t1, r1 = sol[c1][c1_index]
        
        "Delete the course we're currently working with from the list of available c1 courses"
        del c1list[c1list.index(c1)]
        
        'Determine the c1 status'
        if sol[c1][c1_index] == (None,None):
            c1Null = True
        else:
            c1Null = False
        
        'Assemble the list of potential courses to swap with'
        c2list = list(range(0, Courses_max))
        
        "Delete c1 from the list of courses we can swap with, so that we don't swap c1 with itself"
        del c2list[c2list.index(c1)]
        
        'Loop until a successful swap with c2 can be achieved, otherwise choose a new c1'
        while Successful == False:
            'If the list is empty, then there exist no beneficial moves for c1, choose a new c1'
            if len(c2list) == 0:
                data.qua.QL.append(c1)
                data.qua.IL.append(Iter + Gamma)
                print('We are putting', c1, 'in quarantine because it is hard to move it', data.qua.QL)
                # print('newc1',c1list)
                break
            
            'Choose a course from the list of possible swaps, then remove it to prevent repeat iterations'
            c2_index = random.randint(0, len(c2list)-1)
            c2 = c2list[c2_index]
            del c2list[c2_index]
            
            "Determine which dictionary entries are populated, and which aren't, then store these indices"  
            CountP = 0
            CountNP = 0
            pop_list = []
            np_list = []
            
            for i, j in enumerate(sol[c2]):
                if j != (None,None):
                    pop_list.append(i)
                    CountP = CountP + 1
                else:
                    np_list.append(i)
                    CountNP = CountNP + 1
            
            while (len(pop_list) != 0 or len(np_list) != 0) and Successful != True:
                'Call the dictionary for c2 and randomly select the sub-dict to use from the populated entries'        
                if len(pop_list) != 0:
                    pop_index = random.randint(0, len(pop_list)-1)
                    c2_index = pop_list[pop_index]
                    t2, r2 = sol[c2][c2_index]
                    
                    c2Null = False

                    del pop_list[pop_index]
                    
                elif len(pop_list) == 0 and len(np_list) != 0:
                    '''If both sol[c1_index] and sol[c2_index] are null entries in sol, find a new c2_index.
                    We iterate through the populated entries first, so there are no other populated options'''
                    if c1Null:
                        break
                    
                    "If we've already tried to drop c1 and it didn't work, there's no point in trying again"
                    if len(np_list) != CountNP:
                        break
                    
                    c2Null = True
                    
                    'Call the dictionary for c2 and randomly select the sub-dict to use from the non-populated entries' 
                    np_index = random.randint(0, len(np_list)-1)
                    c2_index = np_list[np_index]
                    
                    del np_list[np_index]
                
                else:
                    'If both lists are empty, then none of the swaps with c2 are feasible'
                    break
                                     
                #Cases
                #1) Both sol[c1_index] and sol[c2_index] are scheduled --> SWAP
                #2) Only sol[c2_index] is scheduled --> ADD
                #3) Only sol[c1_index] is scheduled --> DROP
                #4) Neither are scheduled --> not permitted, handled earlier in the code
                
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
                        if Feasibility_Check(c2, t1, r1, ProvTimetable, Courses_max, F_ct, data)\
                        and Feasibility_Check(c1, t2, r2, ProvTimetable, Courses_max, F_ct, data):
                            
                            ProvTimetable[c1, t2, r2] = 1
                            ProvTimetable[c2, t1, r1] = 1
                            
                            'Check if the objective is better'
                            ProvObj = Set_obj(data, ProvTimetable)
                            if ProvObj < Obj:
                                Successful = True
                                print("CASE 1: Swap\nNew obj = ", ProvObj)
                                print("Previous obj = ", Obj)
                                data.qua.QL.append(c1)
                                data.qua.IL.append(Iter + Sigma)
                                data.qua.QL.append(c2)
                                data.qua.IL.append(Iter + Sigma)
                                print('We are putting', c1, c2, 'in quarantine because they have just been moved',
                                      data.qua.QL, data.qua.IL)
                                #print('newc1',c1list)
                                break
                         
                elif c1Null == True and c2Null == False:
                    'CASE 2: sol[c1_index] is unscheduled and sol[c2_index] is non-null --> add sol[c1_index] at random'
                    
                    'We need to iterate between all possible combinations of t2, r2'
                    Possibilities = list(product(list(range(total_timeslots)), list(range(rooms_max))))
                    
                    'We iterate while there are still potential replacements in the list, break on a success'
                    while len(Possibilities) != 0 and Successful != True:
                        'Initialize the t2 and r2 to be used for the current iteration'
                        poss_index = random.randint(0, len(Possibilities)-1)
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
                                    print("CASE 2: Add\nNew obj = ", ProvObj)
                                    print("Previous obj = ", Obj)
                                    data.qua.QL.append(c1)
                                    data.qua.IL.append(Iter + Sigma)
                                    print('We are putting', c1, 'in quarantine because it has just been moved',
                                          data.qua.QL)

                                    break
                else:
                    'CASE 3: sol[c1_index] is non-null and sol[c2_index] is unscheduled --> drop c1'
                    
                    'If all two layers of checks are successful, implement the change, else choose new c2_index'
                    #'Continue the evaluation only if the move is not on the tabu list'
                    #if CheckTab[c1, t2, r2]:
                            
                    'Create the provisional timetable to evaluate the new objective'
                    ProvTimetable = copy.deepcopy(timetable)
                    ProvTimetable[c1, t1, r1] = 0
                        
                    ProvObj = Set_obj(data, ProvTimetable)
                    
                    'Check if the objective is better'
                    if ProvObj < Obj:
                        Successful = True
                        print("CASE 3: Drop\nNew obj = ", ProvObj)
                        print("Previous obj = ", Obj)
                        # data.qua.QL.append(c1)
                        # data.qua.IL.append(Iter+Sigma)
                        #????????????????????????????????
                        break                
                        
    #Cases
    #1) Both sol_entry and c1 are scheduled --> SWAP
    #2) Only sol_entry is scheduled --> ADD
    #3) Only c1 scheduled --> DROP
    #4) Neither are scheduled --> not permitted, handled earlier in the code

    if Successful == True:
        print(" (c1, t1, r1) = ", c1, ", ", t1, ", ", r1, "\n", "(c2, t2, r2) = ", c2, ", ", t2,
              ", ", r2)
    
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
        
    return Optimum

# ciao = swap(data.sol, data.timetable, CurrentObj, data.Courses_max, data.total_timeslots, data.rooms_max, data.F_ct, data.Chi_cc,data)
