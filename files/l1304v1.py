#!/bin/python
###############################################
# File Name : l1304v1.py
#    Author : rootkiter
#    E-mail : rootkiter@rootkiter.com
#   Created : Wed 16 Oct 2016 12:25:57 AM PDT
###############################################

packetsize=1304
regsize=1304
packet={
    #  field-name  ,  type  ,  offset  , default_value 
    "cmdgroup"    :[  "u32" ,  0x00    , 1              ],
    "threads"     :[  "u32" ,  4+0x88  , 1              ],


    "min"         :[  "u32" ,  4+0x90  , 1              ],

    "dnstarget"   :[  "str" ,  0xFC    , "192.168.119.1"],
    "dnsflag"     :[  "u32" ,  0x114   , 1              ],
    "dnsflag2"    :[  "u32" ,  0x514   , 1              ],

    "brrowTime"   :[  "u32" ,  1292    , 1              ],
    "brrowPort"   :[  "u32" ,  1288    , 909            ],
    "brrowUrl"    :[  "str" ,  1032    , "192.168.119.1"]
}

testcase={    
    "dnsflood":{
            "fieldname":["cmdgroup","threads","dnstarget",'min',"dnsflag","dnsflag2"],
            "valuefix" :{"cmdgroup":"0x10"}
    },
    "brrow":{
            "fieldname":["cmdgroup","brrowTime","brrowPort","brrowUrl"],
            "valuefix" :{"cmdgroup":"0x0F"}
    },
    "stop":{
            "fieldname":["cmdgroup"],
            "valuefix" :{"cmdgroup":"0x09"}
    },
    "clean":{
            "fieldname":["cmdgroup"],
            "valuefix" :{"cmdgroup":"0x0D"}
    }
}
#C:\Program Files\Internet Explorer\iexplore.exe baidu.com/


cmdhelp={
    '''cc_cmdway:
        '162a9a13a734c757bb71b34d19558889'
    '''
}

sampleList=[
    '162a9a13a734c757bb71b34d19558889','test sample'
]