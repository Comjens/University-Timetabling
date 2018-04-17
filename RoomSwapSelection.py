# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 18:25:30 2018

@author: james.david
"""
import random
from OptimValueDelta import Set_obj_delta
from FeasibilityCheck import Feasibility_Check
import copy

def RoomSwapSelection(Data, rPriorityList, rlist, tlist, c1, c1_index, c1Null, CurrentObj, t_old, r_old):
    FeasCount = 0
    FeasMax = 30
    ObjectiveList = []
    
    if len(rPriorityList) == 0:
        print("Priority room list is empty")
    if len(rlist) == 0:
        print("Regular room list is empty")
    
    #Cycle through all required instances of t1 such that we acquire the desired number of feasible solutions
    while FeasCount != FeasMax:
        #If none of the timeslots are beneficial, exit to the upper program
        if len(tlist) == 0:
            print("Could only find ", FeasCount, " feasible solutions when ", FeasMax, " were requested")
            break
        
        #Select the timeslot to be fixed (t1) and delete it from the candidate list
        t1_index = random.randint(0, len(tlist)-1)
        t1 = tlist[t1_index]
        del tlist[t1_index]
        
        rCount = 0

        #Feasibility has already been handled in creating the tlist and rlist candidate lists, so we need not test it
        #For a given t1, we cycle through all possibilities of r in the rPriorityList
        while rCount != (len(rPriorityList) + len(rlist)) and FeasCount != FeasMax:
            
            #Select the room list we will operate upon
            if rCount == 0 and len(rPriorityList) != 0:
                UsedList = rPriorityList
            else:
                UsedList = rlist
                
            for r in UsedList:           
                rCount = rCount + 1
                
                #Check if a course already exists in the target room durng timeslot t1
                c2Null = True
                for c in range(Data.Courses_max):
                    if Data.timetable[(c, t1, r)] != 0:
                        c2Null = False
                        c2 = c
                
                if c2Null == False and c1Null == False:
                    Data.timetable[(c1, t_old, r_old)] = 0
                    Data.timetable[(c2, t1, r)] = 0
                    
                    #Check the feasibility of the moves
                    if Feasibility_Check(c2, t_old, r_old, Data) and Feasibility_Check(c1, t1, r, Data):
                        FeasCount = FeasCount + 1
                        
                        Data.timetable[(c1, t_old, r_old)] = 1
                        Data.timetable[(c2, t1, r)] = 1
                        
                        #Calculate the provisional objective
                        Obj = Set_obj_delta(Data, ((c2, t1, r),(c2, t_old, r_old)), ((c1, t_old, r_old),(c1, t1, r)))  
                        ObjectiveList.append((Obj, t1, r, c2Null, c2))
                        
                        if FeasCount == FeasMax:
                            break     
                    else:
                        Data.timetable[(c1, t_old, r_old)] = 1
                        Data.timetable[(c2, t1, r)] = 1
                        
                elif c2Null == False and c1Null == True:
                    Data.timetable[(c2, t1, r)] = 0
                    
                    if Feasibility_Check(c1, t1, r, Data):
                        #Feasibility is always possible for drops (c2), feasibility is passively ensured already for c1
                        FeasCount = FeasCount + 1
                        
                        Data.timetable[(c2, t1, r)] = 1
                        
                        #Calculate the provisional objective
                        Obj = Set_obj_delta(Data, ((c2, t1, r),(c2, t_old, r_old)), ((c1, t_old, r_old),(c1, t1, r)))  
                        ObjectiveList.append((Obj, t1, r, c2Null, c2))
                        
                        if FeasCount == FeasMax:
                            break     
                    else:
                        Data.timetable[(c2, t1, r)] = 1
                else:
                    Data.timetable[(c1, t_old, r_old)] = 0
                    
                    if Feasibility_Check(c1, t1, r, Data):
                        FeasCount = FeasCount + 1
                        
                        Data.timetable[(c1, t_old, r_old)] = 1
                        
                        #Calculate the provisional objective
                        Obj = Set_obj_delta(Data, ((c1, t_old, r_old),(c1, None, None)), ((c1, None, None),(c1, t1, r)))
                        ObjectiveList.append((Obj, t1, r, c2Null, None))
                        
                        if FeasCount == FeasMax:
                            break 
                    else:
                        Data.timetable[(c1, t_old, r_old)] = 1
                        
    
    Accepted = False
    
    if len(ObjectiveList) == 0:
        print("No feasible solutions found")
    else:
        #Perform the best swap discovered
        ObjectiveList.sort(key=lambda elem: elem[0])
        Obj_index = 0
        
        #Iterate until we can perform a move
        while not Accepted:
            
            if Obj_index == len(ObjectiveList):
                print("Could not perform a successful swap due to the taboo list")
                break
            
            CurrentObj, t1, r1, c2Null, c2 = ObjectiveList[Obj_index]
            
            if CurrentObj < Data.BestObj:
                print("NEW BEST!")
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
                    
                    print("(c2, t1, r1) = ", c2, t1, r1)
                    print("Performed STANDARD SWAP operation")
                    
                elif not c2Null and c1Null:
                    Data.timetable[(c2, t1, r1)] = 0
                    Data.timetable[(c1, t1, r1)] = 1
                    
                    Data.sol[c1][c1_index] = (t1, r1)
                    Data.sol[c2][(Data.sol[c2]).index((t1, r1))] = (t_old, r_old)
                    
                    Data.tab.AddTab((c1, t_old, r_old), Data)
                    Data.tab.AddTab((c2, t1, r1), Data)
                    
                    print("(c2, t1, r1) = ", c2, t1, r1)
                    print("Performed NULL SWAP operation")
                    
                else:
                    Data.timetable[(c1, t_old, r_old)] = 0
                    Data.timetable[(c1, t1, r1)] = 1     
                    
                    Data.sol[c1][c1_index] = (t1, r1)
                    
                    Data.tab.AddTab((c1, t_old, r_old), Data)
                    
                    print("(c1, t1, r1) = ", c1, t1, r1)
                    print("Performed MOVE operation")
                
                Data.BestObj = CurrentObj
                Data.BestSol = copy.deepcopy(Data.sol)
                
            else:
                print("Kept previous objective")
                
                if not c2Null and not c1Null and not Data.tab.CheckTab((c2, t_old, r_old)) and not Data.tab.CheckTab((c1, t1, r1)):
                    Data.timetable[(c1, t_old, r_old)] = 0
                    Data.timetable[(c2, t1, r1)] = 0
                    Data.timetable[(c1, t1, r1)] = 1
                    Data.timetable[(c2, t_old, r_old)] = 1
                    
                    Data.sol[c1][c1_index] = (t1, r1)
                    Data.sol[c2][(Data.sol[c2]).index((t1, r1))] = (t_old, r_old)
                    
                    Data.tab.AddTab((c1, t_old, r_old), Data)
                    Data.tab.AddTab((c2, t1, r1), Data)
                    
                    print("(c2, t1, r1) = ", c2, t1, r1)
                    print("Performed STANDARD SWAP operation")
                    
                    Accepted = True
                    
                elif not c2Null and c1Null and not Data.tab.CheckTab((c2, t_old, r_old)) and not Data.tab.CheckTab((c1, t1, r1)):
                    Data.timetable[(c2, t1, r1)] = 0
                    Data.timetable[(c1, t1, r1)] = 1
                    
                    Data.sol[c1][c1_index] = (t1, r1)
                    Data.sol[c2][(Data.sol[c2]).index((t1, r1))] = (t_old, r_old)
                    
                    Data.tab.AddTab((c1, t_old, r_old), Data)
                    Data.tab.AddTab((c2, t1, r1), Data)
                    
                    print("(c2, t1, r1) = ", c2, t1, r1)
                    print("Performed NULL SWAP operation")
                    
                    Accepted = True
                    
                elif not Data.tab.CheckTab((c1, t1, r1)):
                    Data.timetable[(c1, t_old, r_old)] = 0
                    Data.timetable[(c1, t1, r1)] = 1     
                    
                    Data.sol[c1][c1_index] = (t1, r1)
                    
                    Data.tab.AddTab((c1, t_old, r_old), Data)
                    
                    print("(c1, t1, r1) = ", c1, t1, r1)
                    print("Performed MOVE operation")
                    
                    Accepted = True
                    
                else:
                    print("(c1, t_old, r_old) = ", c1, t_old, r_old)
                    print("(c2, t1, r1) = ", c2, t1, r1)
                    print(ObjectiveList[Obj_index])
                    print("Proposed a TABOO move, recoursing to a different entry")
            
            Obj_index = Obj_index + 1
        
        print("Best Objective = ", Data.BestObj)    
        print("Current Objective = ", CurrentObj)   
    
    return CurrentObj, Accepted

