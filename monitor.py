# -*- coding: utf-8 -*-
'''
Created on 2017. 12. 22.
@author: HyechurnJang
'''

import json
import gevent
import gevent.monkey
from platforms import Logstash, C3, AWS
from pygics import Task

gevent.monkey.patch_all()

LOGSTASH_IP = '192.168.56.254'
C3_IP = '211.245.65.143'
C3_USER = 'cliqradmin'
C3_KEY = '6BA257A8F62F3D97'

ls = Logstash(LOGSTASH_IP)
c3 = C3(C3_IP, C3_USER, C3_KEY)
aws = AWS()

def doAgent():
    #===========================================================================
    # 1. Get VM Desc
    #===========================================================================
    print 'start get vms'
    vms = c3.getVMs()
    
    #===========================================================================
    # 2. Get Cloud Statistics
    #===========================================================================
    print 'start get metrics'
    aws.getMetric(vms['amazon'])
    
    #===========================================================================
    # 3. Push to ELK
    #===========================================================================
    print 'start send to logstash'
    ls.send(vms['amazon'])
    
    print 'finish'

class Monitor(Task):
    
    def __init__(self):
        Task.__init__(self, tick=30)
        self.start()
    
    def __run__(self): doAgent()

Monitor().idle()