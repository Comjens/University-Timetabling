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

def BasicSwapAsp(datau, CurrentObj, Iteration):
    
    #Initiate the c1 candidate list
    c1list = list(range(0, datau.Courses_max))
    ObjectiveList = []
    FeasMax = 30
    FeasCount = 0

    #Choose the c1 to be worked with
    c1 = c1list[random.randint(0, len(c1list) - 1)]
    
    #Choose the lecture in the sol dictionary that will be assessed
    c1_lectures = list(enumerate(datau.sol[c1]))
    local_index = random.randint(0, len(c1_lectures)-1)
    c1_index, (t_old, r_old) = c1_lectures[local_index]
    
    if (t_old, r_old) == (None, None):
        c1Null = True
    else:
        c1Null = False
    
    print("(c1, t_old, r_old) = ", c1, t_old, r_old)
        
    Possibilities = list(product(list(range(datau.total_timeslots)), list(range(datau.rooms_max))))
    
    while len(Possibilities) != 0 and FeasCount != FeasMax:
        
        #Choose the entries in the Possibilities list
        poss_index = random.randint(0, len(Possibilities) - 1)
        t1, r1 = Possibilities[poss_index]
        del Possibilities[poss_index]
        
        #Check if a course already exists in the target room durng timeslot t1
        c2Null = True
        for c in range(datau.Courses_max):
            if datau.timetable[(c, t1, r1)] != 0:
                c2Null = False
                c2 = c
        
        if c2Null == False and c1Null == False:
            datau.timetable[(c1, t_old, r_old)] = 0
            datau.timetable[(c2, t1, r1)] = 0
            
            #Check the feasibility of the moves
            if Feasibility_Check(c1, t1, r1, datau) and Feasibility_Check(c2, t_old, r_old, datau):
                FeasCount = FeasCount + 1
                
                datau.timetable[(c1, t_old, r_old)] = 1
                datau.timetable[(c2, t1, r1)] = 1
                
                #Calculate the provisional objective
                Obj = Set_obj_delta(datau,((c2, t1, r1),(c2, t_old, r_old)), ((c1, t_old, r_old),(c1, t1, r1)))  
                ObjectiveList.append((Obj, t1, r1, c2Null, c2))
                
            else:
                datau.timetable[(c1, t_old, r_old)] = 1
                datau.timetable[(c2, t1, r1)] = 1
                
        elif c2Null == False and c1Null == True:
            datau.timetable[(c2, t1, r1)] = 0
            
            #Check the feasibility of the moves
            if Feasibility_Check(c1, t1, r1, datau):
                FeasCount = FeasCount + 1
                
                datau.timetable[(c2, t1, r1)] = 1
                
                #Calculate the provisional objective
                Obj = Set_obj_delta(datau, ((c2, t1, r1),(c2, t_old, r_old)), ((c1, t_old, r_old),(c1, t1, r1)))  
                ObjectiveList.append((Obj, t1, r1, c2Null, c2))
                
            else:
                datau.timetable[(c2, t1, r1)] = 1
        else:
            if Feasibility_Check(c1, t1, r1, datau):
                FeasCount = FeasCount + 1
                
                #Calculate the provisional objective
                Obj = Set_obj_delta(datau, ((c1, t_old, r_old),(c1, None, None)), ((c1, None, None),(c1, t1, r1)))
                ObjectiveList.append((Obj, t1, r1, c2Null, None))
                        
    #Perform the best swap discovered
    ObjectiveList.sort(key=lambda elem: elem[0])
    
    Accepted = False
    Obj_index = 0
    
    #Iterate until we can perform a move
    while not Accepted:
        
        CurrentObj, t1, r1, c2Null, c2 = ObjectiveList[Obj_index]
        
        if CurrentObj < datau.BestObj:
            print("NEW BEST!")
            Accepted = True
            
            if not c2Null:
                datau.timetable[(c1, t_old, r_old)] = 0
                datau.timetable[(c2, t1, r1)] = 0
                datau.timetable[(c1, t1, r1)] = 1
                datau.timetable[(c2, t_old, r_old)] = 1
                
                datau.sol[c1][c1_index] = (t1, r1)
                datau.sol[c2][(datau.sol[c2]).index((t1, r1))] = (t_old, r_old)
                
                if not datau.tab.CheckTab((c2, t_old, r_old, datau)):
                    datau.tab.AddTab((c2, t_old, r_old), datau)
                    
                if not datau.tab.CheckTab((c1, t1, r1, datau)):
                    datau.tab.AddTab((c1, t1, r1), datau)
                
                print("(c2, t1, r1) = ", c2, t1, r1)
                print("Performed SWAP operation")
            
            else:
                datau.timetable[(c1, t_old, r_old)] = 0
                datau.timetable[(c1, t1, r1)] = 1     
                
                datau.sol[c1][c1_index] = (t1, r1)
                
                if not datau.tab.CheckTab((c1, t1, r1, datau)):
                    datau.tab.AddTab((c1, t1, r1), datau)
                
                print("(c1, t1, r1) = ", c1, t1, r1)
                print("Performed MOVE operation")
            
            datau.BestObj = CurrentObj
            datau.BestSol = copy.deepcopy(datau.sol)
            
        else:
            print("Kept previous objective")
            
            if not c2Null and not datau.tab.CheckTab((c2, t_old, r_old, datau)) and not datau.tab.CheckTab((c1, t1, r1, datau)):
                datau.timetable[(c1, t_old, r_old)] = 0
                datau.timetable[(c2, t1, r1)] = 0
                datau.timetable[(c1, t1, r1)] = 1
                datau.timetable[(c2, t_old, r_old)] = 1
                
                datau.sol[c1][c1_index] = (t1, r1)
                datau.sol[c2][(datau.sol[c2]).index((t1, r1))] = (t_old, r_old)
                
                datau.tab.AddTab((c1, t1, r1), datau)
                datau.tab.AddTab((c2, t_old, r_old), datau)
                
                print("(c2, t1, r1) = ", c2, t1, r1)
                print("Performed SWAP operation")
                
                Accepted = True
                
            elif not datau.tab.CheckTab((c1, t1, r1, datau)):
                datau.timetable[(c1, t_old, r_old)] = 0
                datau.timetable[(c1, t1, r1)] = 1     
                
                datau.sol[c1][c1_index] = (t1, r1)
                
                datau.tab.AddTab((c1, t1, r1), datau)
                
                print("(c1, t1, r1) = ", c1, t1, r1)
                print("Performed MOVE operation")
                
                Accepted = True
                
            else:
                print("Proposed a TABOO move, recoursing to a different entry")
        
        Obj_index = Obj_index + 1
    
    print("Best Objective = ", datau.BestObj)    
    print("Current Objective = ", CurrentObj)   
    return CurrentObj, Iteration
            
def BasicSwap(datau, CurrentObj, Iteration):
    
    #Initiate the c1 candidate list
    c1list = list(range(0, datau.Courses_max))
    ObjectiveList = []
    FeasMax = 10
    FeasCount = 0

    #Choose the c1 to be worked with
    c1 = c1list[random.randint(0, len(c1list) - 1)]
    
    #Choose the lecture in the sol dictionary that will be assessed
    
    c1_lectures = list(enumerate(datau.sol[c1]))
    local_index = random.randint(0, len(c1_lectures)-1)
    c1_index, (t_old, r_old) = c1_lectures[local_index]
    
    if (t_old, r_old) == (None, None):
        c1Null = True
    else:
        c1Null = False
    
    print("(c1, t_old, r_old) = ", c1, t_old, r_old)
        
    Possibilities = list(product(list(range(datau.total_timeslots)), list(range(datau.rooms_max))))
    
    for t, r in Possibilities:
        if datau.tab.CheckTab((c1, t, r, datau)):
            del Possibilities[Possibilities.index((t, r))]
    
    while len(Possibilities) != 0 and FeasCount != FeasMax:
        
        #Choose the entries in the Possibilities list
        poss_index = random.randint(0, len(Possibilities) - 1)
        t1, r1 = Possibilities[poss_index]
        del Possibilities[poss_index]
        
        #Check if a course already exists in the target room durng timeslot t1
        c2Null = True
        for c in range(datau.Courses_max):
            if datau.timetable[(c, t1, r1)] != 0:
                c2Null = False
                c2 = c
        
        if c2Null == False and c1Null == False:
            datau.timetable[(c1, t_old, r_old)] = 0
            datau.timetable[(c2, t1, r1)] = 0
            
            #Check the feasibility of the moves
            if Feasibility_Check(c1, t1, r1, datau) and Feasibility_Check(c2, t_old, r_old, datau):
                FeasCount = FeasCount + 1
                
                datau.timetable[(c1, t_old, r_old)] = 1
                datau.timetable[(c2, t1, r1)] = 1
                
                #Calculate the provisional objective
                Obj = Set_obj_delta(datau, ((c2, t1, r1),(c2, t_old, r_old)), ((c1, t_old, r_old),(c1, t1, r1)))  
                ObjectiveList.append((Obj, t1, r1, c2Null, c2))
                
            else:
                datau.timetable[(c1, t_old, r_old)] = 1
                datau.timetable[(c2, t1, r1)] = 1
                
        elif c2Null == False and c1Null == True:
            datau.timetable[(c2, t1, r1)] = 0
            
            #Check the feasibility of the moves
            if Feasibility_Check(c1, t1, r1, datau):
                FeasCount = FeasCount + 1
                
                datau.timetable[(c2, t1, r1)] = 1
                
                #Calculate the provisional objective
                Obj = Set_obj_delta(datau, ((c2, t1, r1),(c2, t_old, r_old)), ((c1, t_old, r_old),(c1, t1, r1)))  
                ObjectiveList.append((Obj, t1, r1, c2Null, c2))
                
            else:
                datau.timetable[(c1, t_old, r_old)] = 1
                datau.timetable[(c2, t1, r1)] = 1
            
        else:
            if Feasibility_Check(c1, t1, r1, datau):
                FeasCount = FeasCount + 1
                
                #Calculate the provisional objective
                Obj = Set_obj_delta(datau, ((c1, t_old, r_old),(c1, None, None)), ((c1, None, None),(c1, t1, r1)))
                ObjectiveList.append((Obj, t1, r1, c2Null, None))
                        
    #Perform the best swap discovered
    ObjectiveList.sort(key=lambda elem: elem[0])
    CurrentObj, t1, r1, c2Null, c2 = ObjectiveList[0]
        
    if not c2Null:
        datau.timetable[(c1, t_old, r_old)] = 0
        datau.timetable[(c2, t1, r1)] = 0
        datau.timetable[(c1, t1, r1)] = 1
        datau.timetable[(c2, t_old, r_old)] = 1
        datau.sol[c1][c1_index] = (t1, r1)
        
        datau.sol[c2][(datau.sol[c2]).index((t1, r1))] = (t_old, r_old)
        
        datau.tab.AddTab((c2, t_old, r_old), datau)
        datau.tab.AddTab((c1, t1, r1), datau)
        
        print("(c2, t1, r1) = ", c2, t1, r1)
        print("Performed SWAP operation")
    
    else:
        datau.timetable[(c1, t_old, r_old)] = 0
        datau.timetable[(c1, t1, r1)] = 1     
        datau.sol[c1][c1_index] = (t1, r1)
        
        datau.tab.AddTab((c1, t1, r1), datau)
        
        print("(c1, t1, r1) = ", c1, t1, r1)
        print("Performed MOVE operation")
        
    if CurrentObj < datau.BestObj:
        print("NEW BEST!")
        datau.BestObj = CurrentObj
        datau.BestSol = copy.deepcopy(datau.sol)
    else:
        print("Kept previous objective")
    
    print("Best Objective = ", datau.BestObj)    
    print("Current Objective = ", CurrentObj)   
    
    return CurrentObj, Iteration            
            
            
            
            
                            