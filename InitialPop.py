# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 13:12:50 2018

@author: Jens Østergaard
"""

def InitPop(data):
    import random
    from itertools import product
    from FeasibilityCheck import Feasibility_Check
    Placements = 0
    courses = list(range(0, data.Courses_max))

    MinCriteria = min(data.rooms_max * data.total_timeslots, sum([len(data.sol[i]) for i in data.sol]))
    Sorted_list_c = [(sum(data.F_ct[c]), c) for c in range(data.Courses_max)]
    Sorted_list_c.sort()
    #Sorted_list_t = [(sum([i[t] for i in data.F_ct]), t) for t in range(data.total_timeslots)]
    #Sorted_list_t.sort()
    while Placements < data.params['Initiate'] * MinCriteria:

        # Define the initial entry'
        try:

            c1 = Sorted_list_c[-1][1]

            # courses_index = random.randint(0, len(courses) - 1)
        except Exception as e:
            print(e)
            break

        # Assemble the list of indices corresponding to non-populated entries in the solution dictionary
        np_indexlist = []
        CountNP = 0
        for i, j in enumerate(data.sol[c1]):
            if j == (None,None):
                np_indexlist.append(i)
                CountNP = CountNP + 1;
        
        if CountNP == 0:
            # If there are no unscheduled entries, we have no reason to revisit this course for now
            del Sorted_list_c[-1]

        else:
            np = random.randint(0, len(np_indexlist)-1)
            c1_index = np_indexlist[np]
            del np_indexlist[np]

            Possibilities = list(product(list(range(data.total_timeslots)), list(range(data.rooms_max))))
            
            Feasibility = False

            #Probe to see where this lecture may be placed
            while Feasibility == False:
                #If we've iterated through all possibilities and the course cannot be placed, move on
                if len(Possibilities) == 0:
                    del Sorted_list_c[-1]
                    break

                #Randomly generate the timeslot and room, then remove this from the Possibilities list
                p_index = random.randint(0, len(Possibilities)-1)
                t1, r1 = Possibilities[p_index]
                del Possibilities[p_index]

                #Perform a feasibility check, if feasible, schedule the course
                Feasibility = Feasibility_Check(c1, t1, r1, data.timetable,data.Courses_max,data.F_ct,data)
            
                if Feasibility == True:
                    data.sol[c1][c1_index] = (t1, r1)
                    data.timetable[c1, t1, r1] = 1
                    Placements = Placements + 1
