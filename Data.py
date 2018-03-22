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




    def __init__(self, data):
        self.basic = data['basic']
        self.courses = data['courses']
        self.rooms =data['rooms']
        self.relation = data['relation']
        self.unavailability = data['unavailability']

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
        self.sol = {Course: [None for i in range(int(self.courses[Course+1][2]))]
                    for Course in range(self.Courses_max)}

    def set_C_q(self,C_q):
        assert isinstance(C_q, list)
        self.C_q = C_q

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