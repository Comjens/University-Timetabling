import itertools
import random
import time
from multiprocessing import Pool, cpu_count, Manager

import Data
from Differentials import *
from OptimValue import *
# from Parameters import *
from SwapFunction import swap

# multiprocessing.set_start_method('forkserver')
m = Manager()
q = m.Queue()
cores = cpu_count()

DIR = "Data/Test02/"

Setn = ["Data/Test{:02}/".format(i) for i in range(1, 14)]

Alphan = [5, 10, 15]
Betan = [1, 1.25, 1.5, 2]
Gamman = [10, 15, 20]
Deltan = [10, 20, 30]
Sigman = [5, 10, 15]
Epsilonn = [0.99995]
Initiaten = [1]
a = [Setn, Alphan, Betan, Gamman, Deltan, Sigman, Epsilonn, Initiaten]
initList = list(itertools.product(*a))


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


def Optimize(que, initList):
    while True:
        try:
            params = {i: j for i, j in zip(['Set', 'Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma', 'Epsilon', 'Initiate'],
                                           initList[random.randint(1, len(initList) - 1)])}
            files = file_names(params['Set'])
            data = Data(read_file(params['Set'], files), params)
            print("Current Working set: {}".format(params['Set']))
            Set_params(data)
            # print('#courses;', data.Courses_max, '\n#rooms:', data.rooms_max, '\n#timeslots:', data.total_timeslots)
            InitPop(data.sol, data.timetable, data.Courses_max, data.rooms_max, data.total_timeslots, data)
            print(Set_obj(data, data.timetable))
            "Define the percentage of populated entries within the sol dictionary"
            TotLength = min(data.rooms_max * data.total_timeslots,
                            sum([(len(data.sol[i])) for i in range(data.Courses_max)]))
            SolNPLength = sum(
                [1 for i in range(len(data.sol)) for j in range(len(data.sol[i])) if data.sol[i][j] == (None, None)])
            Placement = SolNPLength / TotLength

            CurrentObj = Set_obj(data, data.timetable)
            AllowDecrease = False

            # print(data.sol, "\n")
            # print(Set_obj(data, data.timetable), "\n")
            Iteration = 0
            InitStart = time.time()

            while time.time() - InitStart < 300:
                start = time.time()
                # print("ITERATION: ", Iteration)

                Obj = Set_obj(data, data.timetable)

                LocalOptimum = swap(data.sol, data.timetable, CurrentObj, data.Courses_max, data.total_timeslots,
                                    data.rooms_max, data.F_ct, data.Chi_cc, data, Iteration, Placement, AllowDecrease)
                Iteration = Iteration + 1
                CurrentObj = Set_obj(data, data.timetable)
                AllowDecrease = DifferentialCheck(data.diff, CurrentObj, Obj, data)

                # print("Iteration Runtime: {:.5} s".format(time.time() - start))

                SolNPLength = sum(
                    [1 for i in range(len(data.sol)) for j in range(len(data.sol[i])) if
                     data.sol[i][j] == (None, None)])
                Placement = SolNPLength / TotLength

                # print("The matrix is populated at", 100 * (1 - Placement), "percent")
                # print("Total Runtime: {:.5} s  \n".format(time.time() - InitStart),)
                # if LocalOptimum == True:
                # print("Local Optimum =", LocalOptimum, "\n")
            que.put((params, CurrentObj, Iteration))
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
    else:
        output(PeraFile, message[0], message[1], message[2])
        print("Iteration: {}, solution : {}".format(it, message[1]))
    it += 1
'''