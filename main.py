from OptimValue import *
from Differentials import *
import time
import random
from __global__ import *
from BasicSwap import BasicSwap
from Sort import *

def output(PeraFile, params, CurrentObj, Iteration):
    import datetime, os
    Set = params['Set'][-7:-1]
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
            infile.write("YYYY-MM-DDTHH:MM:SS,Set,Alpha,Beta,Gamma,Delta,Sigma,Epsilon,Initiate,Obj,Iteration")
            infile.write(
                "\n{},{},{},{},{},{},{},{},{},{},{}".format(datetime.datetime.now().isoformat(), Set, Alpha, Beta,
                                                            Gamma, Sigma, Delta, Epsilon, Initiate, CurrentObj,
                                                            Iteration))

    else:  # else it exists so append without writing the header
        with open(PeraFile + ".csv", mode='a') as infile:  # 2018-04-14T16:28:20.102387
            infile.write(
                "\n{},{},{},{},{},{},{},{},{},{},{}".format(datetime.datetime.now().isoformat(), Set, Alpha, Beta,
                                                            Gamma, Delta, Sigma, Epsilon, Initiate, CurrentObj,
                                                            Iteration))


# zip(['Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma', 'Epsilon', 'Initiate'],initList[random.randint(1,len(initList)-1)])
# {i:j for i,j in zip(['Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma', 'Epsilon', 'Initiate'],)}
PeraFile = "TestCases"


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

while (time.time()- verystart) <= 300:
    start = time.time()
    Iteration = Iteration + 1
    print("ITERATION = ", Iteration)
    CurrentObj, Iteration = BasicSwap(datau, CurrentObj, Iteration)
    
    #Obj = Set_obj(datau,datau.timetable)
    
    #PhaseCount, Iteration, CurrentObj, SuccessSwaps = RoomSwapPrep(datau, CurrentObj, Iteration, PhaseCount, SuccessSwaps)
    
    print("Iteration Runtime: {:.5} s\n".format(time.time()-start))
    print("Total Runtime: {:.5} s\n".format(time.time()-start))
       

output(BasicFile, datau.params, CurrentObj, Iteration)        