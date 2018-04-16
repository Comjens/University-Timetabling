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
            self.TIL.append(n2+5)
                
    def CheckTab(self,place):
       return place in self.TL


class Qua:
    QL = []
    IL = []

    def __init__(self, a):
        self.a = a

    def AddQua(self, n1, n2):
        if not self.QL.__contains__((n1,n2)):
            self.QL.append((n1,n2))
            self.IL.append(n2)

    def RemQua(self, place1, place2, place3):
        self.QL.remove((place1,place2))
        self.IL.remove(place3)


class Diff:
    DL = []
    Av = 0

    def __init__(self, a):
        self.a = a

    def AddObj(self, num):
        if len(self.DL) < self.a:
            self.DL.append(num)
        else:
            self.DL.pop(0)
            self.DL.append(num)
        self.Av = sum(self.DL) / float(len(self.DL))
        
        
        
#if len(self.TL)<self.a:
#            self.TL.append(place)
#       else:
#            self.TL.pop(0)
#            self.TL.append(place)'''#
