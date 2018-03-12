import os
from __global__ import *


DIR = "data/Test01/"
files = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]

#print(files)
def read_file(files):
    data = []
    for i in files:
        with open("data/Test01/"+i) as infile:
            RAW = infile.readlines()
        vars()[i[:-4]] = [i.rsplit() for i in RAW]
        data.append(vars()[i[:-4]])
    return data

basic,courses,curricula,lecturers,relation,rooms,unavailabiliy = read_file(files)

print(basic)
print(courses)
print(curricula)
print(lecturers)
print(relation)
print(rooms)
print(unavailabiliy)