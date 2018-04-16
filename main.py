from OptimValue import *
from Differentials import *
import time
import random
from __global__ import *
from BasicSwap import BasicSwap
from OptimValueDelta import *



DIR = "Data/Test02/"

files = file_names(DIR)
datau = Data(read_file(DIR,files))

Set_params(datau)
#print(data.sol,"\n\n\n\n")
#print('#courses;', data.Courses_max,'\n#rooms:', data.rooms_max,'\n#timeslots:',data.total_timeslots) 
InitPop(datau)

CurrentObj = Set_obj(datau,datau.timetable)
datau.BestObj = 9999999



Iteration = 0
PhaseCount = 0
SuccessSwaps = 0

verystart=time.time()
import math
print(CurrentObj)
for i in datau.sol.keys():
    for j in datau.sol[i]:
        sol_i = {"course": i, "day": math.floor(j[0] / datau.days_max), "period": j[0] % datau.days_max,
                "room": j[1]}
        print("C{course:04} {day} {period} R{room:04}".format(**sol_i))

''''
while (time.time()- verystart) <= 30:
    start = time.time()
    Iteration = Iteration + 1
    print("ITERATION = ", Iteration)
    CurrentObj, Iteration = BasicSwap(datau, CurrentObj, Iteration)
    
    #Obj = Set_obj(datau,datau.timetable)
    
    #PhaseCount, Iteration, CurrentObj, SuccessSwaps = RoomSwapPrep(datau, CurrentObj, Iteration, PhaseCount, SuccessSwaps)
    
    print("Iteration Runtime: {:.5} s\n".format(time.time()-start))
'''
#data.
#print("C{course:04} {day} {period} R{room:04}".format(sol_i))