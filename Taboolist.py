from Sort import SortChiComplexity
#from main2 import *
from Data import *
class Taboo:
    TL = []
    TIL = []
    def __init__(self,a):
        self.a=a

    def AddTab(self,place,data):
        n2=SortChiComplexity(data,place)
        if not self.TL.__contains__(place):
            self.TL.append(place)
            self.TIL.append(n2*data.params['Delta'] + 10)

    def CheckTab(self,place):
       return place in self.TL
   
    def RemTab(self,place1, place2):
        self.TL.remove(place1)
        self.TIL.remove(place2)
        


class Qua:
    QL = []
    IL = []

    def __init__(self, a):
        self.a = a

    def AddQua(self, n1, n2):
        if not self.QL.__contains__(n1):
            self.QL.append(n1)
            self.IL.append(n2)

    def RemQua(self, place1, place3):
        self.QL.remove(place1)
        self.IL.remove(place3)


class Diff:
    DL = []
    Av = 0

    def __init__(self, a):
        self.a = a
    
    def AddObj(self, num):
        if len(self.DL) < 30:
            self.DL.append(num)
        else:
            self.DL.pop(0)
            self.DL.append(num)

        self.Av = sum(self.DL) / float(len(self.DL))    
    def Flat(self, d):
        coun=0
        k= len(self.DL)-1
        while k>=0:
            if self.DL[k] >= 0:
                coun=coun+1
            else:
                coun=0
                return False
            if coun==10:
                return True
            else:
                k=k-1

