from OptimValue import *
from Differentials import *
import time
import random
from __global__ import *
from BasicSwap import BasicSwap, BasicSwapAsp
from Sort import *
from OptimValueDelta import *
from RoomSwapPrep import RoomSwapPrep
from TimeslotSwapPrep import TimeslotSwapPrep
from SwapChoice import *
import math

def output(PeraFile, params, CurrentObj, Iteration,InitialObj):
    import datetime, os
    Set = 'Test02'
    Alpha = params['Alpha']
    Beta = params['Beta']
    Gamma = params['Gamma']
    Sigma = params['Sigma']
    Delta = params['Delta']
    Epsilon = params['Epsilon']
    Initiate = params['Initiate']

    # with open(PeraFile,mode = 'a+') as infile:
    #    infile.write("{:2},{},{},{},{},{},{},{}".format(datetime.datetime.now().isoformat(),alpha,beta,gamma,sigma,epsilon,init,data.CurrentObj,Iteration)
    if not os.path.isfile(PeraFile + ".csv"):
        with open(PeraFile + ".csv", mode='w+') as infile:  # 2018-04-14T16:28:20.102387
            infile.write("YYYY-MM-DDTHH:MM:SS,Set,Alpha,Beta,Gamma,Delta,Sigma,Epsilon,Initiate,InitialObj,Obj,Iteration")
            infile.write(
                "\n{},{},{},{},{},{},{},{},{},{},{},{}".format(datetime.datetime.now().isoformat(), Set, Alpha, Beta,
                                                            Gamma, Sigma, Delta, Epsilon, Initiate, InitialObj, CurrentObj,
                                                            Iteration))

    else:  # else it exists so append without writing the header
        with open(PeraFile + ".csv", mode='a') as infile:  # 2018-04-14T16:28:20.102387
            infile.write(
                "\n{},{},{},{},{},{},{},{},{},{},{},{}".format(datetime.datetime.now().isoformat(), Set, Alpha, Beta,
                                                            Gamma, Delta, Sigma, Epsilon, Initiate, InitialObj, CurrentObj,
                                                            Iteration))


# zip(['Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma', 'Epsilon', 'Initiate'],initList[random.randint(1,len(initList)-1)])
# {i:j for i,j in zip(['Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma', 'Epsilon', 'Initiate'],)}
PeraFile = "TestCasesAdvancedSwap"

#while True:   
verystart=time.time()

DIR = "Data/Test11/"
files = file_names(DIR)
datau = Data(read_file(DIR,files))

Set_params(datau)
InitPop_roomsVsStudents(datau)
print("Initial Objective = ", Set_obj(datau))
InitPop(datau)

CurrentObj = Set_obj(datau)
InitialObj = CurrentObj
datau.BestObj = 9999999
print("Secondary Objective = ", CurrentObj)

Iteration = 0

for i in datau.sol.keys():
    for j in datau.sol[i]:
        try:
            sol_i = {"course": i, "day": math.floor(j[0] / datau.days_max), "period": j[0] % datau.days_max,
                "room": j[1]}
            print("C{course:04} {day} {period} R{room:04}".format(**sol_i))
        except:
            pass

while (time.time()- verystart) <= 16:
    start = time.time()
    Iteration = Iteration + 1
    #print("ITERATION = ", Iteration)
    
    TimePenalty, RoomPenalty = ComputeWorst(datau)

    #print("Time Penalty = {:.4}".format(TimePenalty))
    #print("Room Penalty = {}".format(RoomPenalty))
    
    if TimePenalty > RoomPenalty:
        CurrentObj = TimeslotSwapPrep(datau, CurrentObj, Iteration)
    else:
        CurrentObj = RoomSwapPrep(datau, CurrentObj, Iteration)
    
    #print("Iteration Runtime: {:.5} s\n".format(time.time()-start))
    #print("Total Runtime: {:.5} s\n".format(time.time()-verystart))
       
output(PeraFile, datau.params,CurrentObj, datau.BestObj, Iteration)

for i in datau.sol.keys():
    for j in datau.sol[i]:
        try:
            sol_i = {"course": i, "day": math.floor(j[0] / datau.days_max), "period": j[0] % datau.days_max,
                "room": j[1]}
            print("C{course:04} {day} {period} R{room:04}".format(**sol_i))
        except:
            pass

    
