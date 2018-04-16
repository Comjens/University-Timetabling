from OptimValue import *

from SwapFunction import swap
from Differentials import *
import time
import random
from RoomSwapPrep import RoomSwapPrep
from __global__ import *
from BasicSwap import BasicSwap


DIR = "C:/Users/james.david/Desktop/Research/02_Denmark/01_DTU - Industrial Engineering Management/Semesters/Winter 2018/42137 - Optimization using Metaheuristics/00_Project/Test Data/Test02/"

files = file_names(DIR)
datau = Data(read_file(DIR,files))

Set_params(datau)
#print(data.sol,"\n\n\n\n")
#print('#courses;', data.Courses_max,'\n#rooms:', data.rooms_max,'\n#timeslots:',data.total_timeslots) 
InitPop(datau.sol, datau.timetable, datau.Courses_max, datau.rooms_max, datau.total_timeslots,datau)

CurrentObj = Set_obj(datau,datau.timetable)
datau.BestObj = 9999999



Iteration = 0
PhaseCount = 0
SuccessSwaps = 0

verystart=time.time()

while (time.time()- verystart) <= 500:
    start = time.time()
    Iteration = Iteration + 1
    print("ITERATION = ", Iteration)
    CurrentObj, Iteration = BasicSwap(datau, CurrentObj, Iteration)
    
    #Obj = Set_obj(datau,datau.timetable)
    
    #PhaseCount, Iteration, CurrentObj, SuccessSwaps = RoomSwapPrep(datau, CurrentObj, Iteration, PhaseCount, SuccessSwaps)
    
    print("Iteration Runtime: {:.5} s\n".format(time.time()-start))
       
        