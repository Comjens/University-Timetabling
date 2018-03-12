import os
from __global__ import *
from Solution import *





def file_names(DIR):
    files = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]
    return  sorted(files, key=str.lower)
DIR = "data/Test01/"
files = file_names(DIR)

#print(files)
def read_file(files):
    data = []
    for i in files:
        print(i)
        with open("data/Test01/"+i) as infile:
            RAW = infile.readlines()
        vars()[i[:-4]] = [i.rsplit() for i in RAW]
        data.append(vars()[i[:-4]])
    #print(data)
    return data

basic,courses,curricula,lecturers,relation,rooms,unavailabiliy= read_file(files)
print(basic)
print(courses)
print(curricula)
print(lecturers)
print(relation)
print(rooms)
print(unavailabiliy)


Sol = Solution(basic)

print(Sol.Curricula)

C_q = [[] for q in range(Sol.Curricula)]
for i,j in relation[1:]:
    C_q[int(i[1:])].append(int(j[1:]))

T_d = [Sol.Periods_per_day * i for i in range(Sol.days)]

L_c = [None for i in range (Sol.Courses)]
S_c = [0 for i in range(Sol.Courses)]
M_c = [0 for i in range(Sol.Courses)]
for i,j,k,l,m in courses[1:]:
    L_c[int(i[1:])]=int(k)
    S_c[int(i[1:])]=int(m)
    M_c[int(i[1:])] = int(l)

C_r = [0 for i in range(Sol.rooms)]
for i,j in rooms[1:]:
    C_r[int(i[1:])]=int(j)

F_ct = [[True for i in range(Sol.total_timeslots) ] for j in range(Sol.Courses)]
for i,j,k in unavailabiliy[1:]:
    F_ct[int(i[1:])][int(j)*Sol.Periods_per_day+int(k)-1] = False


print(F_ct[0][23])