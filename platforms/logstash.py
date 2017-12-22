# -*- coding: utf-8 -*-
'''
Created on 2017. 12. 22.
@author: HyechurnJang
'''

import json
import socket

class Logstash:
    
    def __init__(self, ip):
        self.ip = ip
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.sock.connect((self.ip, 8929))
        except Exception as e: print str(e)
        print self.sock
    
    def send(self, vms):
        for vm in vms:
            data = json.dumps(vm) + '\n'
            try: self.sock.send(data)
            except Exception as e: print str(e)
