# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 11:55:29 2018

@author: Jens Østergaard
"""
import numpy as np

def Set_obj_delta(data, swap1, swap2):
    temp_set_tcr = data.timetable.copy()
    temp_set_tcr[swap1[0]],temp_set_tcr[swap2[0]]=0,0
    temp_set_tcr[swap1[1]], temp_set_tcr[swap2[1]] = 1,1
    temp_set_tcr=np.transpose(temp_set_tcr ,axes=(1,0,2))
    # first oenality term how many working day less then the desiderable the lectures are distributed over
    '''temp_set_tcr = np.array(
        [[[1 if ((c, t, r) != swap1[0] and (c, t, r) != swap2[0] and data.timetable[(c, t, r)]) or (c, t, r) ==
               swap1[1] or (c, t, r) == swap2[1] else 0 for r in range(data.rooms_max)] for c in range(data.Courses_max)] for t in
         range(data.total_timeslots)], dtype=int)'''
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
    # sol2 = (1 - sol[:, :, 0]) @ ( T_tt)# + (1 - T_tt.T))
    A_qt = np.zeros((data.Curricula_max, data.total_timeslots))
    for q in range(data.Curricula_max):
        for t in range(data.total_timeslots):
            if sol[q, t] == 1:
                if np.sum(temp_set_tcr[t2,c,r] for c in data.C_q[q] for r in range(data.rooms_max) for t2 in
                       range(data.total_timeslots) if data.T_tt[t][t2] == 1 or data.T_tt[t2][t] == 1) == 0:
                    A_qt[q][t] = 1

    # how many lectures less than the planned ones are scheduled
    Unplanned_c = np.maximum(data.L_c - np.sum(temp_set_tcr, axis=(0, 2)), 0)
    data.set_Unplanned_c(list(Unplanned_c))
    TT_d = np.array([i for i in np.eye(data.days_max) for j in range(data.Periods_per_day)])
    Workingdays_c = np.maximum(
        data.M_c - np.sum(np.sum(TT_d.T @ np.transpose(temp_set_tcr, (1, 0, 2)), axis=2) >= 1, axis=1), 0)

    data.set_Workingdays_c(list(Workingdays_c))
    S_c = np.array(data.S_c)
    V_tr = np.maximum(S_c @ temp_set_tcr - data.C_r, 0)


    # The number of room changes (number of violations of the room stability) by a course c ∈ C is calculated by the function Pc (x):
    P_c = [0 for c in range(data.Courses_max)]
    for c in range(data.Courses_max):
        P_c[c] = max(0, len([r for r in range(data.rooms_max) if
                             sum(temp_set_tcr[t,c,r] >= 1 for t in range(data.total_timeslots))]) - 1)
    data.set_P_c(P_c)

    obj = sum(P_c[c] for c in range(data.Courses_max)) \
          + np.sum(V_tr) + 2 * np.sum(A_qt) + 10 * np.sum(Unplanned_c) + 5 * np.sum(Workingdays_c)

    #print(obj,sum(P_c[c] for c in range(data.Courses_max)),np.sum(V_tr), np.sum(A_qt),np.sum(Unplanned_c),np.sum(Workingdays_c))
    return obj
