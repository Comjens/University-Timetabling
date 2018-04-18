# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 13:50:12 2018

@author: james.david
"""
from itertools import product
import random
import copy
from OptimValueDelta import Set_obj_delta
from FeasibilityCheck import Feasibility_Check

def BasicSwapAsp(Data, CurrentObj, Iteration):
    #Initiate the c1 candidate list
    c1list = list(range(0, Data.Courses_max))
    ObjectiveList = []
    FeasMax = 30
    FeasCount = 0

    #Choose the c1 to be worked with
    c1 = c1list[random.randint(0, len(c1list) - 1)]
    
    #Choose the lecture in the sol dictionary that will be assessed
    c1_lectures = list(enumerate(Data.sol[c1]))
    local_index = random.randint(0, len(c1_lectures)-1)
    c1_index, (t_old, r_old) = c1_lectures[local_index]
    
    if (t_old, r_old) == (None, None):
        c1Null = True
    else:
        c1Null = False
    
    Possibilities = list(product(list(range(Data.total_timeslots)), list(range(Data.rooms_max))))
    
    while len(Possibilities) != 0 and FeasCount != FeasMax:
        #Choose the entries in the Possibilities list
        poss_index = random.randint(0, len(Possibilities) - 1)
        t1, r1 = Possibilities[poss_index]
        del Possibilities[poss_index]
        
        #Check if a course already exists in the target room durng timeslot t1
        c2Null = True
        for c in range(Data.Courses_max):
            if Data.timetable[(c, t1, r1)] != 0:
                c2Null = False
                c2 = c
        
        if c2Null == False and c1Null == False:
            Data.timetable[(c1, t_old, r_old)] = 0
            Data.timetable[(c2, t1, r1)] = 0
            
            #Check the feasibility of the moves
            if Feasibility_Check(c2, t_old, r_old, Data) and Feasibility_Check(c1, t1, r1, Data):
                FeasCount = FeasCount + 1
                Data.timetable[(c1, t_old, r_old)] = 1
                Data.timetable[(c2, t1, r1)] = 1
                
                #Calculate the provisional objective
                Obj = Set_obj_delta(Data, ((c2, t1, r1),(c2, t_old, r_old)), ((c1, t_old, r_old),(c1, t1, r1)))  
                ObjectiveList.append((Obj, t1, r1, c2Null, c2))
                
                if FeasCount == FeasMax:
                    break     
            else:
                Data.timetable[(c1, t_old, r_old)] = 1
                Data.timetable[(c2, t1, r1)] = 1
                
        elif c2Null == False and c1Null == True:
            Data.timetable[(c2, t1, r1)] = 0
            
            if Feasibility_Check(c1, t1, r1, Data):
                #Feasibility is always possible for drops (c2), feasibility is passively ensured already for c1
                FeasCount = FeasCount + 1
                Data.timetable[(c2, t1, r1)] = 1
                
                #Calculate the provisional objective
                Obj = Set_obj_delta(Data, ((c2, t1, r1),(c2, t_old, r_old)), ((c1, t_old, r_old),(c1, t1, r1)))  
                ObjectiveList.append((Obj, t1, r1, c2Null, c2))
                
                if FeasCount == FeasMax:
                    break     
            else:
                Data.timetable[(c2, t1, r1)] = 1
        else:
            Data.timetable[(c1, t_old, r_old)] = 0
            
            if Feasibility_Check(c1, t1, r1, Data):
                FeasCount = FeasCount + 1
                
                Data.timetable[(c1, t_old, r_old)] = 1
                
                #Calculate the provisional objective
                Obj = Set_obj_delta(Data, ((c1, t_old, r_old),(c1, None, None)), ((c1, None, None),(c1, t1, r1)))
                ObjectiveList.append((Obj, t1, r1, c2Null, None))
                
                if FeasCount == FeasMax:
                    break 
            else:
                Data.timetable[(c1, t_old, r_old)] = 1
                       
    Accepted = False
    
    if len(ObjectiveList) == 0:pass
    else:
        #Perform the best swap discovered
        ObjectiveList.sort(key=lambda elem: elem[0])
        Obj_index = 0
        
        #Iterate until we can perform a move
        while not Accepted:
            if Obj_index == len(ObjectiveList):
                break
            
            CurrentObj, t1, r1, c2Null, c2 = ObjectiveList[Obj_index]
            
            if CurrentObj < Data.BestObj:
                Accepted = True
                
                if not c2Null and not c1Null:
                    Data.timetable[(c1, t_old, r_old)] = 0
                    Data.timetable[(c2, t1, r1)] = 0
                    Data.timetable[(c1, t1, r1)] = 1
                    Data.timetable[(c2, t_old, r_old)] = 1
                    Data.sol[c1][c1_index] = (t1, r1)
                    Data.sol[c2][(Data.sol[c2]).index((t1, r1))] = (t_old, r_old)
                    Data.tab.AddTab((c1, t_old, r_old), Data)
                    Data.tab.AddTab((c2, t1, r1), Data)            

                elif not c2Null and c1Null:
                    Data.timetable[(c2, t1, r1)] = 0
                    Data.timetable[(c1, t1, r1)] = 1
                    Data.sol[c1][c1_index] = (t1, r1)
                    Data.sol[c2][(Data.sol[c2]).index((t1, r1))] = (t_old, r_old)
                    Data.tab.AddTab((c1, t_old, r_old), Data)
                    Data.tab.AddTab((c2, t1, r1), Data)
                    
                else:
                    Data.timetable[(c1, t_old, r_old)] = 0
                    Data.timetable[(c1, t1, r1)] = 1     
                    Data.sol[c1][c1_index] = (t1, r1)
                    Data.tab.AddTab((c1, t_old, r_old), Data)

                Data.BestObj = CurrentObj
                Data.BestSol = copy.deepcopy(Data.sol)
                
            else:
                if not c2Null and not c1Null and not Data.tab.CheckTab((c2, t_old, r_old)) and not Data.tab.CheckTab((c1, t1, r1)):
                    Data.timetable[(c1, t_old, r_old)] = 0
                    Data.timetable[(c2, t1, r1)] = 0
                    Data.timetable[(c1, t1, r1)] = 1
                    Data.timetable[(c2, t_old, r_old)] = 1
                    Data.sol[c1][c1_index] = (t1, r1)
                    Data.sol[c2][(Data.sol[c2]).index((t1, r1))] = (t_old, r_old)
                    Data.tab.AddTab((c1, t_old, r_old), Data)
                    Data.tab.AddTab((c2, t1, r1), Data)
                    Accepted = True
                    
                elif not c2Null and c1Null and not Data.tab.CheckTab((c2, t_old, r_old)) and not Data.tab.CheckTab((c1, t1, r1)):
                    Data.timetable[(c2, t1, r1)] = 0
                    Data.timetable[(c1, t1, r1)] = 1
                    Data.sol[c1][c1_index] = (t1, r1)
                    Data.sol[c2][(Data.sol[c2]).index((t1, r1))] = (t_old, r_old)
                    Data.tab.AddTab((c1, t_old, r_old), Data)
                    Data.tab.AddTab((c2, t1, r1), Data)
                    Accepted = True
                    
                elif not Data.tab.CheckTab((c1, t1, r1)):
                    Data.timetable[(c1, t_old, r_old)] = 0
                    Data.timetable[(c1, t1, r1)] = 1     
                    Data.sol[c1][c1_index] = (t1, r1)
                    Data.tab.AddTab((c1, t_old, r_old), Data)
                    Accepted = True

            Obj_index = Obj_index + 1
    return CurrentObj, Iteration
            
def BasicSwap(Data, CurrentObj, Iteration):
    #Initiate the c1 candidate list
    c1list = list(range(0, Data.Courses_max))
    ObjectiveList = []
    FeasMax = 30
    FeasCount = 0
    #Choose the c1 to be worked with
    c1 = c1list[random.randint(0, len(c1list) - 1)]
    c1_lectures = list(enumerate(Data.sol[c1]))
    local_index = random.randint(0, len(c1_lectures)-1)
    c1_index, (t_old, r_old) = c1_lectures[local_index]
    
    if (t_old, r_old) == (None, None):
        c1Null = True
    else:
        c1Null = False
    Possibilities = list(product(list(range(Data.total_timeslots)), list(range(Data.rooms_max))))
    
    for t, r in Possibilities:
        if Data.tab.CheckTab((c1, t, r)):
            del Possibilities[Possibilities.index((t, r))]
    
    while len(Possibilities) != 0 and FeasCount != FeasMax:
        #Choose the entries in the Possibilities list
        poss_index = random.randint(0, len(Possibilities) - 1)
        t1, r1 = Possibilities[poss_index]
        del Possibilities[poss_index]
        #Check if a course already exists in the target room durng timeslot t1
        c2Null = True
        for c in range(Data.Courses_max):
            if Data.timetable[(c, t1, r1)] != 0:
                c2Null = False
                c2 = c
        
        if c2Null == False and c1Null == False:
            Data.timetable[(c1, t_old, r_old)] = 0
            Data.timetable[(c2, t1, r1)] = 0
            #Check the feasibility of the moves
            if Feasibility_Check(c1, t1, r1, Data) and Feasibility_Check(c2, t_old, r_old, Data):
                FeasCount = FeasCount + 1
                
                Data.timetable[(c1, t_old, r_old)] = 1
                Data.timetable[(c2, t1, r1)] = 1
                
                #Calculate the provisional objective
                Obj = Set_obj_delta(Data, ((c2, t1, r1),(c2, t_old, r_old)), ((c1, t_old, r_old),(c1, t1, r1)))  
                ObjectiveList.append((Obj, t1, r1, c2Null, c2))
                
            else:
                Data.timetable[(c1, t_old, r_old)] = 1
                Data.timetable[(c2, t1, r1)] = 1
                
        elif c2Null == False and c1Null == True:
            Data.timetable[(c2, t1, r1)] = 0
            
            #Check the feasibility of the moves
            if Feasibility_Check(c1, t1, r1, Data):
                FeasCount = FeasCount + 1
                
                Data.timetable[(c2, t1, r1)] = 1
                
                #Calculate the provisional objective
                Obj = Set_obj_delta(Data, ((c2, t1, r1),(c2, t_old, r_old)), ((c1, t_old, r_old),(c1, t1, r1)))  
                ObjectiveList.append((Obj, t1, r1, c2Null, c2))
                
            else:
                Data.timetable[(c2, t1, r1)] = 1
            
        else:
            if Feasibility_Check(c1, t1, r1, Data):
                FeasCount = FeasCount + 1
                
                #Calculate the provisional objective
                Obj = Set_obj_delta(Data, ((c1, t_old, r_old),(c1, None, None)), ((c1, None, None),(c1, t1, r1)))
                ObjectiveList.append((Obj, t1, r1, c2Null, None))
        
    if len(ObjectiveList) == 0:pass
    else:                  
        #Perform the best swap discovered
        ObjectiveList.sort(key=lambda elem: elem[0])
        CurrentObj, t1, r1, c2Null, c2 = ObjectiveList[0]
            
        if not c2Null and not c1Null:
            Data.timetable[(c1, t_old, r_old)] = 0
            Data.timetable[(c2, t1, r1)] = 0
            Data.timetable[(c1, t1, r1)] = 1
            Data.timetable[(c2, t_old, r_old)] = 1
            Data.sol[c1][c1_index] = (t1, r1)
            Data.sol[c2][(Data.sol[c2]).index((t1, r1))] = (t_old, r_old)
            Data.tab.AddTab((c1, t_old, r_old), Data)
            Data.tab.AddTab((c2, t1, r1), Data)

        elif not c2Null and c1Null:
            Data.timetable[(c2, t1, r1)] = 0
            Data.timetable[(c1, t1, r1)] = 1
            Data.sol[c1][c1_index] = (t1, r1)
            Data.sol[c2][(Data.sol[c2]).index((t1, r1))] = (t_old, r_old)
            Data.tab.AddTab((c1, t_old, r_old), Data)
            Data.tab.AddTab((c2, t1, r1), Data)

        else:
            Data.timetable[(c1, t_old, r_old)] = 0
            Data.timetable[(c1, t1, r1)] = 1     
            Data.sol[c1][c1_index] = (t1, r1)
            Data.tab.AddTab((c1, t_old, r_old), Data)

        Data.BestObj = CurrentObj
        Data.BestSol = copy.deepcopy(Data.sol)

    return CurrentObj, Iteration            
