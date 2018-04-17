# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 13:14:34 2018

@author: james.david
"""
from Sort import *
from TimeslotSwapSelection import TimeslotSwapSelection
import random
 
def TimeslotSwapPrep(Data, CurrentObj):
    Possible = True
    print("TIMESLOT SWAP")
       
    #Determine the c1 candidate list
    c1list = SortTimeDomain(Data, 0.05)
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
        
        Addition = False
        if Data.F_ct[c1][t] != 1:
            
            if sum(Data.timetable[(c1,t,r)] for r in range(Data.rooms_max)) < 1:

                for c in range(Data.Courses_max):
                    if Data.Chi_cc[c1][c] != 1 and sum(Data.timetable[(c1,t,r)] for r in range(Data.rooms_max)) < 1:
                        Addition = True
               
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
           
    #print("tlist = ", tlist)
    #print("rlist = ", rlist)
    #print("Priority List = ", rPriorityList)

    if len(tlist) == 0:
        print("Course ", c1, " cannot be moved to any other timeslot")
        #PLACE THIS COURSE ON A COURSE QUARANTINE LIST
        Possible = False
    
    if len(rPriorityList) == 0 and len(rlist) == 0:
        print("c1 = ", c1, " has no possible rooms with which to move")
        Possible = False
    
    if Possible:
        CurrentObj, Accepted = TimeslotSwapSelection(Data, rPriorityList, rlist, tlist, c1, c1_index, c1Null, CurrentObj, t_old, r_old)
        if Accepted == False:
            print("Could not move c1 = ", c1)
    else:
        print("Could not move c1 = ", c1)
   
    return CurrentObj