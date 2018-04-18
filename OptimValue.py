# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 11:55:29 2018

@author: maite
"""
import numpy as np

#InitPop
import numpy as np
import time

def Set_obj(data):
    #first oenality term how many working day less then the desiderable the lectures are distributed over
    temp_set_tcr = np.array(
        [[[data.timetable[(c, t, r)] for r in range(data.rooms_max)] for c in range(data.Courses_max)] for t in
         range(data.total_timeslots)], dtype=int)
    one = np.ones((1, data.rooms_max))
    C_q = np.zeros((data.Curricula_max, data.Courses_max))
    for i, j in data.relation[1:]:
        C_q[int(i[1:]), int(j[1:])] = 1
    T_d = [[time for time in range(data.Periods_per_day * i, data.Periods_per_day * (i + 1))] for i in
           range(data.days_max)]

    T_tt = np.array([[0 for t in range(data.total_timeslots)] for t1 in range(data.total_timeslots)])
    for d in range(data.days_max):
        for t in T_d[d]:
            if t < max(T_d[d]) - 1:
                T_tt[t][t + 1] = 1
    sol = np.dot(C_q, temp_set_tcr) @ one.T
    #sol2 = (1 - sol[:, :, 0]) @ ( T_tt)# + (1 - T_tt.T))
    A_qt = np.zeros((data.Curricula_max,data.total_timeslots))
    for q in range(data.Curricula_max):
        for t in range(data.total_timeslots):
            if sol[q, t] == 1:
                if sum(data.timetable[(c, t2, r)] for c in data.C_q[q] for r in range(data.rooms_max) for t2 in
                       range(data.total_timeslots) if data.T_tt[t][t2] == 1 or data.T_tt[t2][t] == 1) == 0:
                    A_qt[q][t] = 1
    data.set_A_qt(list(A_qt))
    # how many lectures less than the planned ones are scheduled
    Unplanned_c = np.maximum(data.L_c - np.sum(temp_set_tcr, axis=(0, 2)), 0)
    data.set_Unplanned_c(list(Unplanned_c))
    TT_d = np.array([i for i in np.eye(data.days_max) for j in range(data.Periods_per_day)])
    Workingdays_c=np.maximum(data.M_c - np.sum(np.sum(TT_d.T @ np.transpose(temp_set_tcr, (1, 0, 2)), axis=2) >= 1, axis=1), 0)

    data.set_Workingdays_c(list(Workingdays_c))
    S_c = np.array(data.S_c)
    V_tr = np.maximum(S_c @ temp_set_tcr - data.C_r, 0)
    data.set_V_tr(list(V_tr))
    
    #The number of room changes (number of violations of the room stability) by a course c ∈ C is calculated by the function Pc (x): 
    P_c= [0 for c in range(data.Courses_max)]
    for c in range(data.Courses_max):
        P_c[c] = max(0, len([r for r in range(data.rooms_max) if
                             sum(data.timetable[(c, t, r)] >= 1 for t in range(data.total_timeslots))]) - 1)
    data.set_P_c(P_c)

    obj =     sum(P_c[c] for c in range(data.Courses_max)) \
    + np.sum(V_tr) + 2 * np.sum(A_qt) + 10 * np.sum(Unplanned_c) + 5 * np.sum(Workingdays_c)

    return obj#,sum(P_c[c] for c in range(data.Courses_max)),np.sum(V_tr), np.sum(A_qt),np.sum(Unplanned_c),np.sum(Workingdays_c)

    #====================================================================================================


# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 11:55:29 2018

@author: maite
"""


# InitPop

def Set_obj_right(data):
    # first oenality term how many working day less then the desiderable the lectures are distributed over
    Workingdays_c = [0 for i in range(data.Courses_max)]
    for i in range(data.Courses_max):
        a = 0;
        for d in range(data.days_max):
            if (sum(data.timetable[(i, t, r)] for r in range(data.rooms_max) for t in data.T_d[d]) >= 1):
                a = a + 1
        Workingdays_c[i] = max(0, (data.M_c[i] - a))
    data.set_Workingdays_c(Workingdays_c)

    # how many lectures less than the planned ones are scheduled
    Unplanned_c = [0 for i in range(data.Courses_max)]
    for i in range(data.Courses_max):
        Unplanned_c[i] = max(0, data.L_c[i] - sum(
            data.timetable[(i, t, r)] for t in range(data.total_timeslots) for r in range(data.rooms_max)))
    data.set_Unplanned_c(Unplanned_c)

    # the amount of capacity that room r ∈ R is exceeded in time slot t ∈ T:
    V_tr = [[0 for r in range(data.rooms_max)] for t in range(data.total_timeslots)]
    for t in range(data.total_timeslots):
        for r in range(data.rooms_max):
            V_tr[t][r] = max(0,
                             sum([data.timetable[(c, t, r)] * data.S_c[c] for c in range(data.Courses_max)]) - data.C_r[r])
    data.set_V_tr(V_tr)
    # print(V_tr)

    import numpy as np
    temp_set_ctr = np.array(
        [[[data.timetable[(c, t, r)] for r in range(data.rooms_max)] for c in range(data.Courses_max)] for t in
         range(data.total_timeslots)], dtype=int)
    one = np.ones((1, data.rooms_max))
    C_q = np.zeros((data.Curricula_max, data.Courses_max))
    for i, j in data.relation[1:]:
        C_q[int(i[1:]), int(j[1:])] = 1
    T_d = [[time for time in range(data.Periods_per_day * i, data.Periods_per_day * (i + 1))] for i in
           range(data.days_max)]

    T_tt = np.array([[0 for t in range(data.total_timeslots)] for t1 in range(data.total_timeslots)])
    for d in range(data.days_max):
        for t in T_d[d]:
            if t < max(T_d[d]) - 1:
                T_tt[t][t + 1] = 1
    sol = np.dot(C_q, temp_set_ctr) @ one.T
    # sol2 = (1 - sol[:, :, 0]) @ ( T_tt)# + (1 - T_tt.T))
    A_qt = np.zeros((data.Curricula_max, data.total_timeslots))
    for q in range(data.Curricula_max):
        for t in range(data.total_timeslots):
            if sol[q, t] == 1:
                if sum(data.timetable[(c, t2, r)] for c in data.C_q[q] for r in range(data.rooms_max) for t2 in
                       range(data.total_timeslots) if data.T_tt[t][t2] == 1 or data.T_tt[t2][t] == 1) == 0:
                    A_qt[q][t] = 1
    data.set_A_qt(list(A_qt))

    # The number of room changes (number of violations of the room stability) by a course c ∈ C is calculated by the function Pc (x):
    P_c = [0 for c in range(data.Courses_max)]
    for c in range(data.Courses_max):
        P_c[c] = max(0, len([r for r in range(data.rooms_max) if
                             sum(data.timetable[(c, t, r)] >= 1 for t in range(data.total_timeslots))]) - 1)
    data.set_P_c(P_c)

    obj = sum(5 * Workingdays_c[c] + 10 * Unplanned_c[c] + P_c[c] for c in range(data.Courses_max)) + sum(
        V_tr[t][r] for t in range(data.total_timeslots) for r in range(data.rooms_max)) + 2 * sum(
        A_qt[q][t] for q in range(data.Curricula_max) for t in range(data.total_timeslots))

    return obj#,sum(P_c[c] for c in range(data.Courses_max))#,np.sum(V_tr), np.sum(A_qt),np.sum(Unplanned_c),np.sum(Workingdays_c)
    # ====================================================================================================

# print(data)
