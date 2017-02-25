#!/bin/python
###############################################
# File Name : Tester.py
#    Author : rootkiter
#    E-mail : rootkiter@rootkiter.com
#   Created : 02/25 17:36:40 2017
###############################################

from ClassBuilder import *

class Student(ClassBuilder):
    _fields=[
        ('Name','str'),
        ('Age' ,"u16"),
    ]

if __name__=="__main__":
    tt=Student()
    tt.set_Name("XiaoLi")
    tt.set_Age (20)

    ttjson=tt.buildJSON()
    print ttjson

    print "----------------------"

    t2=Student()
    t2.loadJSON(ttjson)
    print t2.get_Name()
    print t2.get_Age()
