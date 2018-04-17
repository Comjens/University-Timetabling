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

def output(PeraFile, params, CurrentObj, Iteration):
    import datetime, os
    Set = params['Set']
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

while True:   
    DIR = "Data/Test{:02}/".format(random.randint(1,13))
    
    files = file_names(DIR)
    datau = Data(read_file(DIR,files))
    datau.params["Set"] = DIR[-7:-1]
    print(datau.params["Set"])
    Set_para(datau)
    print(Set_obj(datau))
    #print(data.sol,"\n\n\n\n")
    #print('#courses;', data.Courses_max,'\n#rooms:', data.rooms_max,'\n#timeslots:',data.total_timeslots) 
    InitPop_roomsVsStudents(datau)
    InitPop(datau)
    CurrentObj = Set_obj(datau)
    InitialObj = CurrentObj
    datau.BestObj = 9999999
    print(CurrentObj)
    
    verystart=time.time()
    import math
    
    Iteration = 0
    
    verystart=time.time()
    

    while (time.time()- verystart) <= 300:
        print(datau.params["Set"])
        start = time.time()
        Iteration = Iteration + 1
        print("ITERATION = ", Iteration)
        
        CurrentObj = RoomSwapPrep(datau, CurrentObj, Iteration)
        
        #CurrentObj, Iteration = BasicSwapAsp(datau, CurrentObj, Iteration)
    
        print("Iteration Runtime: {:.5} s\n".format(time.time()-start))
        print("Total Runtime: {:.5} s\n".format(time.time()-verystart))
           
    output(PeraFile, datau.params, datau.BestObj, Iteration)

    for i in datau.BestSol.keys():
        for j in datau.sol[i]:
            try:
                sol_i = {"course": i, "day": math.floor(j[0] / datau.days_max), "period": j[0] % datau.days_max,
                    "room": j[1]}
                print("C{course:04} {day} {period} R{room:04}".format(**sol_i))
            except:
                pass

    print(datau.params["Set"])
