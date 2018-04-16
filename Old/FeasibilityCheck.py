# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 13:45:35 2018

@author: Maite
"""

def Feasibility_Check(c1, t1, r1, timetable, Courses_max, F_ct, data):
    Feasibility = True
    
    '''CONSTRAINT 1: Only one room per lecture (implictly satisfied) and only if the course is available
    in that timeslot'''
    if F_ct[c1][t1] == 1:
        Feasibility = False
        
    'CONSTRAINT 2: Ensure that no other courses are planned in room r1'
    if sum(timetable[(c,t1,r1)] for c in range(Courses_max))!= 0:
        Feasibility = False
        
    'CONSTRAINT 3: Each course must not exceed the total number of allowable lectures'
    #This constraint is waived as the sol dictionary controls this implicitly
    
    'CONSTRAINT 4: Conflicting courses are not allowed to be scheduled in the same timeslot'
    for c in range(Courses_max):
        if data.Chi_cc[c1][c] == 1 and sum(timetable[(c,t1,r)] for r in range(data.rooms_max)) >= 1:
            Feasibility = False

    return Feasibility

