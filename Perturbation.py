from Sort import SortBoth
from InitialPop import*
import random
from FeasibilityCheck import Feasibility_Check
from OptimValue import *
#1)distroy a part of the sol e rebuilt

#2)move n out of the 30 more terrible moves



def Pert(datau): 
    #create a list of 30 promising courses
    CourseOld=SortBoth(datau)
    Courses = CourseOld[0:30]

    count=0
    #while len(Courses)!=0 and count<=params['K']:
    while len(Courses)!=0 and count<30:
        Swap=False
        #choose a c1 from the 30 courses with the highest penalty
        c1_index = random.randint(0, len(Courses))
        c1=Courses[c1_index-1]

        c1_lectures = list(enumerate(datau.sol[c1]))

        #if the course has lecture take one and delete it from the list, otherwise pick another course and delete the current one from the candidate course list
        if len(c1_lectures) != 0:
            c1lec_index =  random.randint(0, len(c1_lectures))
            c1lec= c1_lectures[c1lec_index-1]
            del c1_lectures[c1lec_index-1]
        else:
            del Courses[c1_index-1]
            break
        
        #create list of feasible t given c1, the two list should be complementary
        tbrutta = []
        tlist = []
        for t in range(datau.total_timeslots):
            Addition = False
            
            if datau.F_ct[c1][t] != 1:  #the fist constraint is ensured here
                Addition =True
                for c2 in range(datau.Courses_max):     #the fourth constraint is ensured here
                    if datau.Chi_cc[c1][c2] == 1 and sum([datau.timetable[(c2, t, r)] for r in range(datau.rooms_max)]) >= 1:
                        Addition = False
                if sum(datau.timetable[(c1,t,r)] for r in range(datau.rooms_max)) >= 1: #fifth constraint
                        Addition = False
                        
                        
            if Addition == True:
                tlist.append(t)
            else:
                tbrutta.append(t)
        while  len(tlist) != 0 and Swap==False:
            t1_index = random.randint(0, len(tlist))
            t1=tlist[t1_index-1]
            del tlist[t1_index-1]
            rlist = []
            rBrutta = []
            for r in range(datau.rooms_max):
                if datau.S_c[c1] <= datau.C_r[r]:
                    rlist.append(r)
                else:
                    rBrutta.append(r)
            while len(rlist)!=0 and  Swap==False:
                r1_index= random.randint(0, len(rlist))
                r1=rlist[r1_index-1]
                del rlist[r1_index-1]
                CEC2 = False
                if c1lec[1] != (None, None):
                    a,b = c1lec[1]
                    for c2 in range(datau.Courses_max):
                        if datau.timetable[(c2, t1, r1)]==1:
                            CEC2 = True
                            datau.timetable[(c1,a,b)]=0
                            datau.timetable[(c2,t1,r1)]=0
                            Fe = Feasibility_Check(c1,t1,r1,datau)  
                            Fe2 = Feasibility_Check(c2,a,b,datau)
                            if Fe2==False or Fe== False:
                                datau.timetable[(c1,a,b)]=1
                                datau.timetable[(c2,t1,r1)]=1
                            else:
                                datau.timetable[(c2,a,b)]=1
                                datau.timetable[(c1,t1,r1)]=1
                                datau.sol[c2][(datau.sol[c2]).index((t1, r1))] = (a, b)
                                
                    if CEC2 == False:
                        Fe2 = True
                        datau.timetable[(c1,a,b)]=0
                        Fe = Feasibility_Check(c1,t1,r1,datau)  

                else:
                    Fe2= True
                    Fe = Feasibility_Check(c1,t1,r1,datau)

                if Fe2 == True and Fe==True:
                    datau.timetable[(c1,t1,r1)]=1
                    datau.timetable[(c1,a,b)]=0
                    datau.sol[c1][c1lec[0]] = (t1, r1)
                    Swap= True
                    count=count+1
                    break
                    break
                else:
                    datau.timetable[(c1,t1,r1)]=0
                    datau.timetable[(c1,a,b)]=1

    return Set_obj(datau)

                
