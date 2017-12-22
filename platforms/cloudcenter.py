# -*- coding: utf-8 -*-
'''
Created on 2017. 12. 22.
@author: HyechurnJang
'''

import json
import gevent
import requests
from requests.auth import HTTPBasicAuth

class C3:
    
    def __init__(self, ip, user, key):
        self.ip = ip
        self.user = user
        self.key = key
        self.url_jobs = 'https://%s/v1/jobs' % self.ip
        self.url_nodes = self.url_jobs + '/%s/nodes'
        self.auth = HTTPBasicAuth(self.user, self.key)
        self.headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
        
    def getURL(self, url):
        resp = requests.get(url, headers=self.headers, auth=self.auth, verify=False)
        if resp.status_code != 200: raise Exception('could not get URL data')
        return resp.json()
    
    def getNodes(self, vms, jobId, jobName, cloudFamily, environment):
        nodes = self.getURL(self.url_nodes % jobId)['nodes']
        for node in nodes:
            virtualMachines = node['virtualMachines']
            for virtualMachine in virtualMachines:
                if virtualMachine['status'] != 'NodeReady': continue
                desc = {
                    'id' : virtualMachine['id'],
                    'publicIp' : virtualMachine['publicIp'],
                    'privateIp' : virtualMachine['privateIp'],
                    'hostName' : virtualMachine['hostName'],
                    'jobName' : jobName,
                    'environment' : environment,
                    'metric' : {}
                }
                if cloudFamily != 'MultiCloud':
                    desc['cloud'] = cloudFamily
                else:
                    vmId = virtualMachine['id']
                    if vmId[0:2] == 'i-': desc['cloud'] = 'Amazon'
                    else: desc['cloud'] = 'Vmware'
                if desc['cloud'] == 'Vmware': vms['vmware'].append(desc)
                elif desc['cloud'] == 'Amazon': vms['amazon'].append(desc)
                all.append(desc)
    
    def getVMs(self):
        
        def fetch(c3, vms, jobId, jobName, cloudFamily, environment):
            nodes = c3.getURL(c3.url_nodes % jobId)['nodes']
            for node in nodes:
                virtualMachines = node['virtualMachines']
                for virtualMachine in virtualMachines:
                    if virtualMachine['status'] != 'NodeReady': continue
                    desc = {
                        'id' : virtualMachine['id'],
                        'publicIp' : virtualMachine['publicIp'],
                        'privateIp' : virtualMachine['privateIp'],
                        'hostName' : virtualMachine['hostName'],
                        'jobName' : jobName,
                        'environment' : environment,
                        'metric' : {}
                    }
                    if cloudFamily != 'MultiCloud':
                        desc['cloud'] = cloudFamily
                    else:
                        vmId = virtualMachine['id']
                        if vmId[0:2] == 'i-': desc['cloud'] = 'Amazon'
                        else: desc['cloud'] = 'Vmware'
                    if desc['cloud'] == 'Vmware': vms['vmware'].append(desc)
                    elif desc['cloud'] == 'Amazon': vms['amazon'].append(desc)
                    all.append(desc)
        
        all = []
        vmw = []
        aws = []
        azr = []
        vms = {'all' : all, 'vmware' : vmw, 'amazon' : aws, 'azure' : azr}
        fetches = []
        jobs_data = self.getURL(self.url_jobs)['jobs']
        for job_data in jobs_data:
#             jobId = job_data['id']
#             jobName = job_data['name']
#             cloudFamily = job_data['cloudFamily']
#             environment = job_data['environment']
            
            fetches.append(gevent.spawn(fetch, self, vms,
                                        job_data['id'],
                                        job_data['name'],
                                        job_data['cloudFamily'],
                                        job_data['environment']))
        gevent.joinall(fetches)
            
        return vms
