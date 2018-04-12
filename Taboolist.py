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

    def RemQua(self, place1, place2):
        self.QL.remove(place1)
        self.IL.remove(place2)


class Suc:
    SL = []
    ItL = []

    def __init__(self, a):
        self.a = a

    def RemSuc(self, place):
        self.SL.remove(place)
        self.ItL.remove(place)
