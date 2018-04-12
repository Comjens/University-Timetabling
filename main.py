from __global__ import *

from OptimValue import *
from SwapFunction import swap
import time


DIR = "C:/Users/james.david/Desktop/Research/02_Denmark/01_DTU - Industrial Engineering Management/Semesters/Winter 2018/42137 - Optimization using Metaheuristics/00_Project/Test Data/Test01/"
files = file_names(DIR)
data = Data(read_file(files))

Set_params(data)
#print(data.sol,"\n\n\n\n")
 
InitPop(data.sol, data.timetable, data.Courses_max, data.rooms_max, data.total_timeslots,data)

CurrentObj = Set_obj(data,data.timetable)

print(data.sol, "\n")
print(Set_obj(data,data.timetable), "\n")
#print(data.F_ct)

Iteration = 0

while Iteration < 200:
    start = time.time()
    print("ITERATION: ", Iteration)
    
    LocalOptimum = swap(data.sol, data.timetable, CurrentObj, data.Courses_max, data.total_timeslots, data.rooms_max, data.F_ct, data.Chi_cc,data)
    Iteration = Iteration + 1
    CurrentObj = Set_obj(data,data.timetable)
    
    print("Iteration Runtime: {:.5} s\n".format(time.time()-start))
    
    if LocalOptimum == True:
        print("Local Optimum =", LocalOptimum)
        
'''mean = []
Iteration = 0
while Iteration < 200:
    data = Data(read_file(files))
    Set_params(data)    
    InitPop(data.sol, data.timetable, data.Courses_max, data.rooms_max, data.total_timeslots,data)
    start = time.time()
    
    CurrentObj = Set_obj(data,data.timetable)
    mean.append(time.time()-start)
    print("time: ",mean[Iteration],sum(mean)/(Iteration+1))
    Iteration = Iteration + 1
    
        
#print(data.sol, "\n")'''

