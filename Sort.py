def SortRoomDomain(data,k):
    A=[0 for c in range(data.Courses_max)]
    V_trc = [[[0 for c in range(data.Courses_max)] for r in range(data.rooms_max)] for t in range(data.total_timeslots)] 
    for t in range(data.total_timeslots): 
        for r in range(data.rooms_max):
            for c in range(data.Courses_max):
                V_trc[t][r][c] = max (0, (data.timetable[(c,t,r)]*data.S_c[c] - data.C_r[r]))
    for c in range(data.Courses_max):
        A[c] = (sum(V_trc[t][r][c] for t in range(data.total_timeslots) for r in range(data.rooms_max))+data.P_c[c],c)
    A.sort(reverse=True)
    Valuelimit= (A[0][0]-A[data.Courses_max-1][0])*(1-k)
    val=0
    for i in range(data.Courses_max):
        if A[i][0] > Valuelimit:
            val=i
        else:
            break
    return [A[i][1] for i in range(0,val+1)] 
    
              
def SortTimeDomain(data,k):
    A=[0 for c in range(data.Courses_max)]
    for q in range(data.Curricula_max):
        for c in (data.C_q[q]):
            A[c] = (sum(data.A_qt[q][t] for t in range(data.total_timeslots))+data.Workingdays_c[c],c)
    A.sort(reverse=True)
    Valuelimit= (A[0][0]-A[data.Courses_max-1][0])*(1-k)
    val=0
    for i in range(data.Courses_max):
        if A[i][0] > Valuelimit:
            val=i
        else:
            break
    return [A[i][1] for i in range(0,val+1)] 

def SortBoth(data):
    A1=[0 for c in range(data.Courses_max)]
    for q in range(data.Curricula_max):
        for c in (data.C_q[q]):
            A1[c] = (sum(data.A_qt[q][t] for t in range(data.total_timeslots))  +  data.Workingdays_c[c]  +  data.P_c[c]  +  sum(data.V_trc[t][r][c] for t in range(data.total_timeslots) for r in range(data.rooms_max)),c)
    A1.sort(reverse=True)
    return [i[1] for i in A1] 

def SortChiComplexity(data,n2):
    Conf= [0 for c in range(data.Courses_max)]
    for c in range(data.Courses_max):
        Conf[c]=(data.Conflicting_c[c],c)
    Conf.sort(reverse=True)
    b=0
    for c in range(data.Courses_max):
        if Conf[c][1]==n2:
            b=Conf[c][0]
    a = Conf[0][0]-Conf[data.Courses_max-1][0]
    c= a-b
    return b

