# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 11:55:29 2018

@author: Jens Østergaard
"""


def Set_obj_delta(data, swap1, swap2):
    temp_set_ctr = [
        [[1 if ((i, t, r) != swap1[0] and (i, t, r) != swap2[0] and data.timetable[(i, t, r)]) or (i, t, r) ==
               swap1[1] or (i, t, r) == swap2[1] else 0 for r in range(data.rooms_max)] for t in
         range(data.total_timeslots)] for i in range(data.Courses_max)]

    # first oenality term how many working day less then the desiderable the lectures are distributed over
    Workingdays_c = [0 for i in range(data.Courses_max)]
    for c in range(data.Courses_max):
        a = 0;
        for d in range(data.days_max):
            if (sum(temp_set_ctr[c][t][r] for r in range(data.rooms_max) for t in
                    data.T_d[d]) >= 1):
                a = a + 1
        Workingdays_c[c] = max(0, (data.M_c[c] - a))

    # how many lectures less than the planned ones are scheduled
    Unplanned_c = [0 for i in range(data.Courses_max)]
    for c in range(data.Courses_max):
        Unplanned_c[c] = max(0, data.L_c[c] - sum(temp_set_ctr[c][t][r] for t in range(data.total_timeslots) for r in range(data.rooms_max)))

    # the amount of capacity that room r ∈ R is exceeded in time slot t ∈ T:
    V_tr = [[0 for r in range(data.rooms_max)] for t in range(data.total_timeslots)]
    for t in range(data.total_timeslots):
        for r in range(data.rooms_max):
            V_tr[t][r] = max(0, sum(temp_set_ctr[c][t][r]*data.S_c[c] for c in range(data.Courses_max)) - data.C_r[r])

    # determines if a curriculum in a time slot has a secluded lecture i.e. there is no adjacent lecture from the same curriculum
    A_qt = [[0 for t in range(data.total_timeslots)] for q in range(data.Curricula_max)]
    for q in range(data.Curricula_max):
        for t in range(data.total_timeslots):
            if sum(temp_set_ctr[c][t][r] for r in range(data.rooms_max) for c in data.C_q[q]) == 1:
                if sum(temp_set_ctr[c][t2][r] for c in data.C_q[q] for r in
                       range(data.rooms_max) for t2 in range(data.total_timeslots) if data.T_tt[t][t2] == 1 or data.T_tt[t2][t] == 1) == 0:
                    A_qt[q][t] = 1

    # The number of room changes (number of violations of the room stability) by a course c ∈ C is calculated by the function Pc (x):
    P_c = [0 for c in range(data.Courses_max)]
    RO = [0 for r in range(data.rooms_max)]
    for c in range(data.Courses_max):
         P_c[c] = max(0, len([r for r in range(data.rooms_max) if
            sum(temp_set_ctr[c][t][r]  >= 1 for t in range(data.total_timeslots))]) - 1)
    # data.set_P_c(P_c)

    obj = sum(5 * Workingdays_c[c] + 10 * Unplanned_c[c] + P_c[c] for c in range(data.Courses_max))\
    + sum(V_tr[t][r] for t in range(data.total_timeslots) for r in range(data.rooms_max))\
    + 2 * sum(A_qt[q][t] for q in range(data.Curricula_max) for t in range(data.total_timeslots))
    return obj
