class Solution:
    Courses = None
    rooms = None
    days = None
    Periods_per_day = None
    Curricula = None
    constraints = None
    lecturers = None

    def __init__(self,basic):
        # Basic data
        self.Courses = int(basic[1][0])
        self.rooms = int(basic[1][1])
        self.days = int(basic[1][2])
        self.Periods_per_day = int(basic[1][3])
        self.Curricula = int(basic[1][4])
        self.constraints = int(basic[1][5])
        self.lecturers = int(basic[1][6])
        self.total_timeslots = self.days*self.Periods_per_day

        # Solution matrix
        #self.timetable = {(days, period, room):None for period in range(self.Periods_per_day) for days in range(self.days )}
        self.sol={Course:[None for i in range()] for Course in range(self.Courses)}
