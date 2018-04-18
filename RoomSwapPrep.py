# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 13:14:34 2018

@author: james.david
"""
from Sort import *
from RoomSwapSelection import RoomSwapSelection
import random
 
def RoomSwapPrep(Data, CurrentObj, Iteration):
    Possible = True
    #Determine the c1 candidate list
    c1list = SortRoomDomain(Data, 1)
    
    QL = Data.qua.QL
    IL = Data.qua.IL
    TL = Data.tab.TL
    TIL = Data.tab.TIL
    #Update the quarantine list
    k = len(IL) - 1
    while k >= 0:
        if IL[k] == Iteration:
            Data.qua.RemQua(QL[k], IL[k])
        elif QL[k] in c1list:
            del c1list[c1list.index(QL[k])]                        
        k = k - 1
    
    #Update the taboo list
    j= len(TIL)-1
    while j >= 0:
        if TIL[j] == Iteration:
            Data.tab.RemTab(TL[j], TIL[j]) 
        j = j - 1
    
    #If the list is empty after being processed by the quarantine
    if len(c1list) == 0:
        c1list = list(range(0, Data.Courses_max))
        for q in QL:
            del c1list[c1list.index(q)] 
            
        c1 = c1list[random.randint(0, len(c1list)-1)]
    else:
        c1 = c1list[random.randint(0, len(c1list)-1)]
    
    #Select the working lecture to be re-evaluated at random, using the sol dictionary 
    c1_lectures = list(enumerate(Data.sol[c1]))
    local_index = random.randint(0, len(c1_lectures)-1)
    c1_index, (t_old, r_old) = c1_lectures[local_index]
    
    if (t_old, r_old) == (None, None):
        c1Null = True
    else:
        c1Null = False
    
    #Create a candidate list for timeslots based on the course availability Fct and the conflict matrix Chi_cc
    #This section passively ensures timeslot feasibility
    tlist = []      
    for t in range(Data.total_timeslots):
        Addition = True
        if Data.F_ct[c1][t] == 1:
            Addition = False
            
        if sum(Data.timetable[(c1,t,r)] for r in range(Data.rooms_max)) >= 1:
            Addition = False

        for c in range(Data.Courses_max):
            if Data.Chi_cc[c1][c] == 1 and sum(Data.timetable[(c1,t,r)] for r in range(Data.rooms_max)) >= 1:
                Addition = False
               
        if Addition == True:
            tlist.append(t)
            
    #Create a candidate list of rooms based on other c1 placements, the room capacities, and the tabu list
    #This section passively ensures room feasibility
    rlist = []
    rPriorityList = []
    
    for r in range(Data.rooms_max):
        if Data.S_c[c1] <= Data.C_r[r]:
            rlist.append(r)
            
            #Establish the list of priority rooms based on the other rooms that c1 is scheduled in
            #These two lists are to be complimentary, and so the relevant rooms are deleted from rlist
            for t in range(Data.total_timeslots):
                if Data.timetable[(c1, t, r)] == 1 and r not in rPriorityList:
                    rPriorityList.append(r)
                    del rlist[rlist.index(r)]

    if len(tlist) == 0:
        #PLACE THIS COURSE ON A COURSE QUARANTINE LIST
        Possible = False
    
    if len(rPriorityList) == 0 and len(rlist) == 0:
        Possible = False
    
    if Possible:
        CurrentObj, Accepted = RoomSwapSelection(Data, rPriorityList, rlist, tlist, c1, c1_index, c1Null, CurrentObj, t_old, r_old)
        if Accepted == False:
            Data.qua.AddQua(c1, Iteration + Data.params['Gamma'])

    return CurrentObj