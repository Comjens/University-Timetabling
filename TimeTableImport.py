import os

def file_names(DIR):
    files = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]
    return  sorted(files, key=str.lower)


#print(files)
def read_file(DIR, files):
    data = {}
    for i in files:
        with open(DIR + i) as infile:
            RAW = infile.readlines()
        temp = [j.rsplit() for j in RAW]
        data[i[:-4]]= temp
    return data

def Set_params(data):

    C_q = [[] for q in range(data.Curricula_max)]
    for i, j in data.relation[1:]:
        C_q[int(i[1:])].append(int(j[1:]))



    T_d = [[time for time in range(data.Periods_per_day * i,data.Periods_per_day * (i+1))] for i in range(data.days_max)]

    L_c = [None for i in range(data.Courses_max)]
    S_c = [0 for i in range(data.Courses_max)]
    M_c = [0 for i in range(data.Courses_max)]
    Mu_c = [0 for i in range(data.Courses_max)]
    for i, j, k, l, m in data.courses[1:]:
        L_c[int(i[1:])] = int(k)
        S_c[int(i[1:])] = int(m)
        M_c[int(i[1:])] = int(l)
        Mu_c[int(i[1:])] =int(j[1:])
    C_r = [0 for i in range(data.rooms_max)]
    for i, j in data.rooms[1:]:
        C_r[int(i[1:])] = int(j)
    C_l = [[] for l in range(data.lecturers_max)]
    for i, j in enumerate(Mu_c):
        C_l[j].append(i)
        
    F_ct = [[False for i in range(data.total_timeslots)] for j in range(data.Courses_max)]
    for i, j, k in data.unavailability[1:]:
        F_ct[int(i[1:])][int(j) * data.Periods_per_day + int(k)] = True

    
    T_tt = [[0 for t in range(data.total_timeslots)] for t1 in range(data.total_timeslots)]
    for d in range(data.days_max):
        for t in T_d[d]:
            if t<max(T_d[d])-1:
                T_tt[t][t+1]=1 
        
    Chi_cc= [[0 for c in range(data.Courses_max)] for c1 in range(data.Courses_max)]
    for q in range(data.Curricula_max):
        for c1 in C_q[q]:
            for c2 in C_q[q]:
                if (c2!=c1):
                    Chi_cc[c1][c2] = 1
    for l in range(data.lecturers_max):
        for c1 in C_l[l]:
            for c2 in C_l[l]:
                if (c2!=c1):
                    Chi_cc[c1][c2] = 1 
                    
    Conflicting_c= [0 for c in range(data.Courses_max)] 
    for c in range(data.Courses_max):
        Conflicting_c[c] = sum(Chi_cc[c][c1] for c1 in range(data.Courses_max))
    data.set_Conflicting_c(Conflicting_c)      

    V_trc = [[[0 for c in range(data.Courses_max)] for r in range(data.rooms_max)] for t in range (data.total_timeslots)]      
    
    #print(type(C_q))
    data.set_C_q(C_q)
    data.set_C_l(C_l)
    data.set_C_r(C_r)
    data.set_L_c(L_c)
    data.set_S_c(S_c)
    data.set_M_c(M_c)
    data.set_Mu_c(Mu_c)
    data.set_T_d(T_d)
    data.set_F_ct(F_ct)
    data.set_T_tt(T_tt)
    data.set_Chi_cc(Chi_cc)
