from Sort import SortBoth
from InitialPop import*
import random
from FeasibilityCheck import Feasibility_Check
from OptimValue import *
#1)distroy a part of the sol e rebuilt

#2)move n out of the 30 more terrible moves

#==================================================================================================
'''print('PER')
DIR = "Data/Test13/"

files = file_names(DIR)
datau = Data(read_file(DIR,files))
Set_params(datau)
InitPop_roomsVsStudents(datau)
print(Set_obj(datau,datau.timetable))
InitPop(datau)
CurrentObj = Set_obj(datau,datau.timetable)
InitialObj = CurrentObj
datau.BestObj = 9999999
print(CurrentObj)
verystart=time.time()
Iteration = 0'''


def Pert(datau): 
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Perturbatioooooon')
    
    #create a list of 30 promising courses
    CourseOld=SortBoth(datau)
    Courses = CourseOld[0:30]
    Courses2 = CourseOld[30:len(CourseOld)-1]
    #print('Corsi:', Courses)
    
    
    
    
    count=0
    #while len(Courses)!=0 and count<=params['K']:
    while len(Courses)!=0 and count<30:
        Swap=False
        
        #choose a c1 from the 30 courses with the highest penalty
        c1_index = random.randint(0, len(Courses))
        c1=Courses[c1_index-1]
        #del Courses[c1_index-1]
        #print('Course',c1)
    
        c1_lectures = list(enumerate(datau.sol[c1]))
        #print('course c1: ',c1,'\nLectures for c1',c1_lectures)
        
        #if the course has lecture take one and delete it from the list, otherwise pick another course and delete the current one from the candidate course list
        if len(c1_lectures) != 0:
            c1lec_index =  random.randint(0, len(c1_lectures))
            c1lec= c1_lectures[c1lec_index-1]
            #print('abbiamo scelto lecture', c1lec, 'out of ', len(c1_lectures))
            del c1_lectures[c1lec_index-1] 
        else:
            #print('There is no more lecture for c1', len (c1_lectures))
            del Courses[c1_index-1]
            #print('rompo!')
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
        #print('c1:', c1, '\ntbuona: ',tlist,'\ntbrutta:',tbrutta)
        
        #pick a t1 from tlist if is not empty 
        while  len(tlist) != 0 and Swap==False:
            t1_index = random.randint(0, len(tlist))
            t1=tlist[t1_index-1]
            del tlist[t1_index-1]
            #print("Tomeslot", t1)
        
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
                #print("Room", r1)            
                del rlist[r1_index-1]
    
    
                CEC2 = False
                if c1lec[1] != (None, None):
                    a,b = c1lec[1]
                    for c2 in range(datau.Courses_max):
                        if datau.timetable[(c2, t1, r1)]==1:
                            CEC2 = True
                            #print('Il corso C2 è già schedulato nella nostra cella lo spostioamo:',c2,a,b)
                            datau.timetable[(c1,a,b)]=0
                            datau.timetable[(c2,t1,r1)]=0
                            Fe = Feasibility_Check(c1,t1,r1,datau)  
                            #print('LA FEASIBILITA DEL PRIMO è:', Fe)
                            Fe2 = Feasibility_Check(c2,a,b,datau)
                            #print('LA FEASIBILITA DEL SEC è:', Fe2)
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
                        #print('LA FEASIBILITA DEL PRIMO è:', Fe)
                        
                else:
                    Fe2= True
                    #datau.timetable[(c1,a,b)]=0
                    Fe = Feasibility_Check(c1,t1,r1,datau)  
                    #print('LA FEASIBILITA DEL PRIMO è:', Fe)
                    
                #print('la feasib', Fe)
    
                #============================================================ACTUAL SWAP
                
                if Fe2 == True and Fe==True:
                    #print('SWAPPPP')
                    datau.timetable[(c1,t1,r1)]=1
                    datau.timetable[(c1,a,b)]=0
                    datau.sol[c1][c1lec[0]] = (t1, r1)
                    Swap= True
                    #print('count:',count)
                    #print(Set_obj(datau,datau.timetable))
                    count=count+1
                    break
                    break
                else:
                    datau.timetable[(c1,t1,r1)]=0
                    datau.timetable[(c1,a,b)]=1
                    #print('non swappiamo')


    return Set_obj(datau)

                
'''for i in datau.sol.keys():
    for j in datau.sol[i]:
        try:
            sol_i = {"course": i, "day": math.floor(j[0] / datau.days_max), "period": j[0] % datau.days_max,
                "room": j[1]}
            print("C{course:04} {day} {period} R{room:04}".format(**sol_i))
        except:
            pass

            
print(len(Courses),count)                                

                    
                
print(InitialObj,Set_obj(datau,datau.timetable))  '''                  
