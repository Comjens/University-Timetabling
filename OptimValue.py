# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 11:55:29 2018

@author: maite
"""


#InitPop

def Set_obj(data,timetable):
    
    #first oenality term how many working day less then the desiderable the lectures are distributed over
    Workingdays_c = [0 for i in range(data.Courses_max)]
    for i in range(data.Courses_max):
        a = 0;
        for d in range(data.days_max):
            if (sum ( timetable[(i,t,r)] for r in range(data.rooms_max) for t in data.T_d[d]) >=1):
                a=a+1
        Workingdays_c[i]= max(0, (data.M_c[i] -a))
    data.set_Workingdays_c(Workingdays_c)
    
    #how many lectures less than the planned ones are scheduled  
    Unplanned_c = [0 for i in range(data.Courses_max)]
    for i in range(data.Courses_max):
        Unplanned_c[i] = max(0, data.L_c[i] - sum(timetable[(i,t,r)] for t in range(data.total_timeslots) for r in range(data.rooms_max)) )
    data.set_Unplanned_c(Unplanned_c)
    
    # the amount of capacity that room r ∈ R is exceeded in time slot t ∈ T:
    V_tr = [[0 for r in range(data.rooms_max)] for t in range(data.total_timeslots)]
    for t in range(data.total_timeslots): 
        for r in range(data.rooms_max):
            V_tr[t][r] = max (0, sum ([timetable[(c,t,r)]*data.S_c[c] for c in range(data.Courses_max)]) - data.C_r[r])       
    data.set_V_tr(V_tr)
    print(V_tr)
    
    #determines if a curriculum in a time slot has a secluded lecture i.e. there is no adjacent lecture from the same curriculum
    A_qt=  [[0 for t in range(data.total_timeslots)] for q in range(data.Curricula_max)]
    for q in range(data.Curricula_max) :
        for t in range(data.total_timeslots):
            if sum (timetable[(c,t,r)] for r in range(data.rooms_max) for c in data.C_q[q])==1 :
                if sum (timetable[(c,t2,r)] for c in data.C_q[q] for r in range(data.rooms_max) for t2 in range(data.total_timeslots) if data.T_tt[t][t2]==1)==0:
                    A_qt[q][t] = 1 
    data.set_A_qt(A_qt)        
   
    
    #The number of room changes (number of violations of the room stability) by a course c ∈ C is calculated by the function Pc (x): 
    P_c= [0 for c in range(data.Courses_max)]
    for c in range(data.Courses_max):
        P_c[c] = max(0, len([r for r in range(data.rooms_max) if
                             sum(data.timetable[(c, t, r)] >= 1 for t in range(data.total_timeslots))]) - 1)
    data.set_P_c(P_c)

    obj = sum(5 * Workingdays_c[c] + 10 * Unplanned_c[c] + P_c[c] for c in range(data.Courses_max)) + sum(V_tr[t][r] for t in range(data.total_timeslots) for r in range(data.rooms_max)) + 2 * sum(A_qt[q][t] for q in range(data.Curricula_max) for t in range(data.total_timeslots))
    
    
    return obj
    #====================================================================================================

# print(data)
