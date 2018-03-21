import os
from __global__ import *
from Solution import *
from Data import *




def file_names(DIR):
    files = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]
    return  sorted(files, key=str.lower)

DIR = "data/Test01/"
files = file_names(DIR)
#print(files)
def read_file(files):
    data = {}
    for i in files:
        print(i)
        with open("data/Test01/"+i) as infile:
            RAW = infile.readlines()
        temp = [j.rsplit() for j in RAW]
        data[i[:-4]]= temp
    print(data)
    return data

data= read_file(files)
print(data.keys())


def Set_params(data):

    C_q = [[] for q in range(data.Curricula_max)]
    for i, j in data.relation[1:]:
        C_q[int(i[1:])].append(int(j[1:]))

    C_q = [[] for q in range(data.Curricula_max)]
    for i, j in data.relation[1:]:
        C_q[int(i[1:])].append(int(j[1:]))

    T_d = [data.Periods_per_day * i for i in range(data.days_max)]

    L_c = [None for i in range(data.Courses_max)]
    S_c = [0 for i in range(data.Courses_max)]
    M_c = [0 for i in range(data.Courses_max)]
    for i, j, k, l, m in data.courses[1:]:
        L_c[int(i[1:])] = int(k)
        S_c[int(i[1:])] = int(m)
        M_c[int(i[1:])] = int(l)

    C_r = [0 for i in range(data.rooms_max)]
    for i, j in data.rooms[1:]:
        C_r[int(i[1:])] = int(j)

    F_ct = [[True for i in range(data.total_timeslots)] for j in range(data.Courses_max)]
    for i, j, k in data.unavailability[1:]:
        F_ct[int(i[1:])][int(j) * data.Periods_per_day + int(k) - 1] = False
    print(type(C_q))
    data.set_C_q(C_q)
    data.set_C_r(C_r)
    data.set_L_c(L_c)
    data.set_S_c(S_c)
    data.set_M_c(M_c)
    data.set_F_ct(F_ct)




#Sol = Solution(basic)

data = Data(read_file(files))

print(data)
Set_params(data)


print(data.sol)