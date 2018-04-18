from Parameters import Alpha, Delta
from Taboolist import Taboo, Qua, Diff


class Data:
    Courses_max = None
    rooms_max = None
    days_max = None
    Periods_per_day = None
    Curricula_max = None
    constraints_max = None
    lecturers_max = None
    C_q = None
    T_d = None
    L_c = None
    S_c = None
    M_c = None
    C_r = None
    F_ct= None
    Unplanned_c=None
    Workingdays_c=0
    V_tr = None
    A_qt = None
    T_tt = None
    Chi_cc = None
    Conflicting_c = None
    BestObj = None
    room = None
    time1 = None

    def __init__(self, data, params={'Alpha': 30, #length of Diff
 'Beta': 15,  #feasibility moves requires,
 'Delta': 10, #duration in the tabu
 'Epsilon': 0, #FREE PARAMETER
 'Gamma': 5, # 'number of iteration we should keep a course difficult to move in the quarantine list'
 'Initiate': 1, #FREE PARAMETER
 'Sigma': 5,#FREE PARAMETER 
 'K': 30, #perturbation length
 'sek':15}):
        self.basic = data['basic']
        self.courses = data['courses']
        self.rooms =data['rooms']
        self.relation = data['relation']
        self.unavailability = data['unavailability']
        self.params = params

        # Basic data
        
        self.Courses_max = int(self.basic[1][0])
        self.rooms_max = int(self.basic[1][1])
        self.days_max = int(self.basic[1][2])
        self.Periods_per_day = int(self.basic[1][3])
        self.Curricula_max = int(self.basic[1][4])
        self.constraints_max = int(self.basic[1][5])
        self.lecturers_max = int(self.basic[1][6])
        self.total_timeslots = self.days_max * self.Periods_per_day
        

        # Solution matrix
        self.timetable = {(course, timeslot, room):0
                          for room in range(self.rooms_max)
                          for timeslot in range(self.total_timeslots)
                          for course in range(self.Courses_max )}
        self.sol = {Course: [(None, None) for i in range(int(self.courses[Course+1][2]))]
                    for Course in range(self.Courses_max)}
        self.BestSol = {Course: [(None, None) for i in range(int(self.courses[Course + 1][2]))]
                        for Course in range(self.Courses_max)}
        self.tab = Taboo(100)
        self.qua = Qua(100)
        self.diff = Diff(params['Alpha'])
        

    def set_T_tt(self,T_tt):
        assert isinstance(T_tt, list)
        self.T_tt = T_tt
        
    def set_Chi_cc(self,Chi_cc):
        assert isinstance(Chi_cc, list)
        self.Chi_cc = Chi_cc
    
    def set_Conflicting_c(self,Conflicting_c):
        assert isinstance(Conflicting_c, list)
        self.Conflicting_c = Conflicting_c

    def set_C_q(self,C_q):
        assert isinstance(C_q, list)
        self.C_q = C_q
    
    def set_C_l(self,C_l):
        assert isinstance(C_l, list)
        self.C_l = C_l

    def set_T_d(self,T_d):
        assert isinstance(T_d, list)
        self.T_d = T_d

    def set_S_c(self,S_c):
        assert isinstance(S_c, list)
        self.S_c = S_c

    def set_M_c(self,M_c):
        assert isinstance(M_c, list)
        self.M_c = M_c

    def set_L_c(self,L_c):
        assert isinstance(L_c, list)
        self.L_c = L_c

    def set_C_r(self,C_r):
        assert isinstance(C_r, list)
        self.C_r = C_r

    def set_F_ct(self,F_ct):
        assert isinstance(F_ct, list)
        self.F_ct = F_ct
   
    def set_Unplanned_c(self,Unplanned_c):
        assert isinstance(Unplanned_c, list)
        self.Unplanned_c = Unplanned_c
    
    def set_Workingdays_c(self,Workingdays_c):
        assert isinstance(Workingdays_c, list)
        self.Workingdays_c = Workingdays_c
        
    def set_V_tr(self,V_tr):
        assert isinstance(V_tr, list)
        self.V_tr = V_tr
        
    '''def set_V_trc(self,V_trc):
        assert isinstance(V_trc, list)
        self.V_trc = V_trc'''
    
    def set_A_qt(self,A_qt):
        assert isinstance(A_qt, list)
        self.A_qt = A_qt    
        
    def set_Mu_c(self,Mu_c):
        assert isinstance(Mu_c,list)
        self.Mu_c=Mu_c
        
    def set_P_c(self,P_c):
        assert isinstance(P_c, list)
        self.P_c = P_c
        
    def set_room(self,room):
        assert isinstance(room, list)
        self.room = room
        
    def set_time1(self,time1):
        assert isinstance(time1, list)
        self.time1 = time1

        

