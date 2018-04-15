# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 17:11:00 2018

@author: maite
"""



class Taboo:
    TL = []
    def __init__(self,a):
        self.a=a

    def AddTab(self,place):
        if len(self.TL)<self.a:
            self.TL.append(place)
        else:
            self.TL.pop(0)
            self.TL.append(place)
    
    def CheckTab(self,place):
       return place in self.TL


class Qua:
    QL = []
    IL = []

    def __init__(self, a):
        self.a = a

    def AddQua(self, n1, n2):
        if not self.QL.__contains__(n1):
            self.QL.append(n1)
            self.IL.append(n2)

    def RemQua(self, place1, place2):
        self.QL.remove(place1)
        self.IL.remove(place2)


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
