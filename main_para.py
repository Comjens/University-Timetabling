import itertools
import random
import time
from multiprocessing import Pool, cpu_count, Manager
from OptimValue import *
from Differentials import *
import time,sys
import random
from __global__ import *
from BasicSwap import BasicSwap, BasicSwapAsp
from Sort import *
from OptimValueDelta import *
from RoomSwapPrep import RoomSwapPrep
from TimeslotSwapPrep import TimeslotSwapPrep
from SwapChoice import *
import math
import multiprocessing



def output(PeraFile, params, BestObj, Iteration,InitialObj,pp):
    import datetime, os
    Set = params['Set']
    Alpha = params['Alpha']
    Beta = params['Beta']
    Gamma = params['Gamma']
    Sigma = params['Sigma']
    Delta = params['Delta']
    Epsilon = params['Epsilon']
    Initiate = params['Initiate']
    K = params['K']
    pp =pp

    Sek = params['sek']

    # with open(PeraFile,mode = 'a+') as infile:
    #    infile.write("{:2},{},{},{},{},{},{},{}".format(datetime.datetime.now().isoformat(),alpha,beta,gamma,sigma,epsilon,init,data.CurrentObj,Iteration)
    if not os.path.isfile(PeraFile + ".csv"):
        with open(PeraFile + ".csv", mode='w+') as infile:  # 2018-04-14T16:28:20.102387
            infile.write("YYYY-MM-DDTHH:MM:SS,Set,Alpha,Beta,Gamma,Delta,Sigma,Epsilon,Initiate,InitialObj,BestObj,Iteration, Perturbations")
            infile.write(
                "\n{},{},{},{},{},{},{},{},{},{},{},{},{}".format(datetime.datetime.now().isoformat(), Set, Alpha, Beta,
                                                            Gamma, Sigma, Delta, Epsilon, Initiate, InitialObj, BestObj,
                                                            Iteration, pp))

    else:  # else it exists so append without writing the header
        with open(PeraFile + ".csv", mode='a') as infile:  # 2018-04-14T16:28:20.102387
            infile.write(
                "\n{},{},{},{},{},{},{},{},{},{},{},{},{}".format(datetime.datetime.now().isoformat(), Set, Alpha, Beta,
                                                                Gamma, Delta, Sigma, Epsilon, Initiate, InitialObj, BestObj,
                                                                Iteration,pp))

import itertools
import random
import time
from multiprocessing import Pool, cpu_count, Manager
from OptimValue import *
from Differentials import *
import time,sys
import random
from __global__ import *
from BasicSwap import BasicSwap, BasicSwapAsp
from Sort import *
from OptimValueDelta import *
from RoomSwapPrep import RoomSwapPrep
from TimeslotSwapPrep import TimeslotSwapPrep
from SwapChoice import *
from Perturbation import *
import math
import multiprocessing

m = Manager()
q = m.Queue()
cores = 4#cpu_count()

DIR = "Data/Test02/"

Setn = ["Data/Test{:02}/".format(i) for i in range(1, 14)]



Alphan = [5, 10, 15]
Betan = [15,20,25]
Gamman = [10, 15, 20]
Deltan = [1, 2, 3]
Sigman = [5, 10, 15]
Epsilonn = [0.99995]
Initiaten = [1]
Kn=[50,100,150]
sekn=[4]
a = [Setn, Alphan, Betan, Gamman, Deltan, Sigman, Epsilonn, Initiaten,Kn,sekn]
initList = list(itertools.product(*a))






PeraFile = "TestCases"
def Optimize(que, initList):
    while True:
        try:
            params = {i: j for i, j in zip(['Set', 'Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma', 'Epsilon', 'Initiate','K','sek'],
                                           initList[random.randint(1, len(initList) - 1)])}
            files = file_names(params['Set'])
            data = Data(read_file(params['Set'], files), params)
            print("Current Working set: {}".format(params['Set']))
            files = file_names(DIR)
            datau = Data(read_file(DIR, files))
            Set_params(datau)
            InitPop_roomsVsStudents(datau)
            InitPop(datau)
            CurrentObj = Set_obj(datau)
            InitialObj = CurrentObj
            datau.BestObj = 9999999
            Iteration = 0
            Pertu = False
            pp=0

            verystart = time.time()
            while (time.time() - verystart) <= 300:
                start = time.time()
                Iteration = Iteration + 1
                TimePenalty, RoomPenalty = ComputeWorst(datau)
                PrevObj = Set_obj(datau)
                if CurrentObj > data.params['K'] + datau.BestObj and Pertu == False:
                    CurrentObj = Pert(datau)
                    Pertu = True
                    pp=pp+1
                else:
                    Pertu=False
                    if TimePenalty > RoomPenalty:
                        CurrentObj = TimeslotSwapPrep(datau, CurrentObj, Iteration)
                    else:
                        CurrentObj = RoomSwapPrep(datau, CurrentObj, Iteration)
                datau.diff.AddObj(CurrentObj-PrevObj)
                #Pertu = datau.diff.Flat(CurrentObj-PrevObj)

            que.put((params,  datau.BestObj, Iteration,InitialObj,pp))
        except Exception as e:
            que.put(e)
            pass


p = Pool(processes=cores)
workers = p.starmap_async(Optimize, ((q, initList) for i in range(cores)))
it = 1
while True:
    message = q.get()
    if isinstance(message, Exception):
        print(message)
    else:#(params,  datau.BestObj, Iteration,InitialObj,pp)
        #output(PeraFile, params, BestObj, Iteration, InitialObj, pp)
        output(PeraFile, message[0], message[1], message[2],message[3],message[4])
        print("Iteration: {}, solution : {}".format(it, message[1]))
    it += 1
