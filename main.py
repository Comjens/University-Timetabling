from OptimValue import *
from SwapFunction import swap
from __global__ import *

DIR = "data/Test02/"
files = file_names(DIR)
data = Data(read_file(files))

Set_params(data)
#print(data.sol,"\n\n\n\n")
print('#courses;', data.Courses_max, '\n#rooms:', data.rooms_max, '\n#timeslots:', data.total_timeslots)
InitPop(data.sol, data.timetable, data.Courses_max, data.rooms_max, data.total_timeslots,data)

CurrentObj = Set_obj(data,data.timetable)

print(data.sol, "\n")
print(Set_obj(data,data.timetable), "\n")
#print(data.F_ct)

Iteration = 0

while Iteration < 200:
    # start = time.time()
    print("ITERATION: ", Iteration)

    LocalOptimum = swap(data.sol, data.timetable, CurrentObj, data.Courses_max, data.total_timeslots, data.rooms_max,
                        data.F_ct, data.Chi_cc, data, Iteration)
    Iteration = Iteration + 1
    CurrentObj = Set_obj(data,data.timetable)

    # print("Iteration Runtime: {:.5} s\n".format(time.time()-start))
    
    if LocalOptimum == True:
        print("Local Optimum =", LocalOptimum)