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

LOGSTASH_IP = '210.93.172.30'
# C3_IP = '211.245.65.143'
# C3_USER = 'cliqradmin'
# C3_KEY = '6BA257A8F62F3D97'

# c3 = C3(C3_IP, C3_USER, C3_KEY)
ls = Logstash(LOGSTASH_IP)
aws = AWS()

def doAgent():
    #===========================================================================
    # 1. Get VM Desc
    #===========================================================================
    print 'start get vms'
#     vms = c3.getVMs()
    vms = aws.getVMs()
    
    print json.dumps(vms)
    
    #===========================================================================
    # 2. Get Cloud Statistics
    #===========================================================================
    print 'start get metrics'
    aws.getMetric(vms['amazon'])
    
    print json.dumps(vms)
    
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