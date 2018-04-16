from Sort import SortBoth
from main import datau
import random
from FeasibilityCheck import Feasibility_Check
from OptimalValue2 import *
#1)distroy a part of the sol e rebuilt

#2)move n out of the 30 more terrible moves


old=Set_obj(datau,datau.timetable)   
print('Begin')
CourseOld=SortBoth(datau)
Courses = CourseOld[0:30]
print('Corsi:', Courses)


#choose a c1 from the 30 courses with the highest penalty

iteration=30


count=0
while len(Courses)!=0 and count<=iteration:
    Swap=False
    c1_index = random.randint(0, len(Courses))
    c1=Courses[c1_index-1]
    del Courses[c1_index-1]
    print('Course',c1)

    c1_lectures = list(enumerate(datau.sol[c1]))
    #print('course c1: ',c1,'\nLectures for c1',c1_lectures)
    
    if len(c1_lectures) != 0:
        c1lec_index =  random.randint(0, len(c1_lectures))
        #print('abbiamo scelto lecture', c1lec_index, 'out of ', len(c1_lectures))
        c1lec= c1_lectures[c1lec_index-1]
        print("Lecture", c1lec)
        del c1_lectures[c1lec_index-1] 
    else:
        #print('There is no mpre lecture for c1', len (c1_lectures))
        del Courses[c1_index-1]
        print('rompo')
        break
    
    #create list of feasible t given c1
    tbrutta = []
    tlist = []
    for t in range(datau.total_timeslots):
        Addition = False
        
        if datau.F_ct[c1][t] != 1:
            
            for c2 in range(datau.Courses_max):
                if datau.Chi_cc[c1][c2] != 1 and sum([datau.timetable[(c2, t, r)] for r in range(datau.rooms_max)]) < 1:
                    Addition = True
          
        if Addition == True:
            tlist.append(t)
        else:
            tbrutta.append(t)
    #print('c1:', c1, '\nbuona: ',tlist,'\nbrutta:',tbrutta)
    
    while  len(tlist) != 0 and Swap==False:
        t1_index = random.randint(0, len(tlist))
        t1=tlist[t1_index-1]
        del tlist[t1_index-1]
        print("Tomeslot", t1)
    
        #given the c and the t generate a list of rooms  
        rlist = [] 
        rBrutta = []
        #bigenough    
        for r in range(datau.rooms_max):
            if datau.S_c[c1] <= datau.C_r[r]:
                rlist.append(r)
            else:
                rBrutta.append(r)
                    
                       
        #print("tlist = ", tlist)
        #print('tbrutto:',tbrutta)
        #print("rlist = ", rlist)
        #print('romm brutta',rBrutta)
        
        #pick an r 
        while len(rlist)!=0 and  Swap==False:
            r1_index= random.randint(0, len(rlist))
            r1=rlist[r1_index-1]
            del rlist[r1_index-1]
            print("Room", r1)
            
            aiut = False
            if c1lec[1] != (None, None):
                a,b = c1lec[1]
                for c2 in range(datau.Courses_max):
                    if datau.timetable[(c2, t1, r1)]==1:
                        aiut = True
                        print(c2,a,b)
                        datau.timetable[(c1,a,b)]=0
                        Fe = Feasibility_Check(c2,a,b,datau)
                        if Fe==False:
                            datau.timetable[(c1,a,b)]=1
                        else:
                            datau.timetable[(c2,a,b)]=1
                if aiut == False:
                    Fe = True   
            else:
                Fe = True
            #print('la feasib', Fe)
            
            #============================================================ACTUAL SWAP
            
            if Fe == True:
                print('SWAPPPP')
                datau.timetable[(c1,t1,r1)]=1
                datau.timetable[(c1,a,b)]=0
                Swap= True
                print('count:',count)
                print(Set_obj(datau,datau.timetable))
                count=count+1
                break
                break
            else:
                print('non swappiamo')
            
                
                    
                
print(old,Set_obj(datau,datau.timetable))                    
