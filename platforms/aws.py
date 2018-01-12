# -*- coding: utf-8 -*-
'''
Created on 2017. 12. 22.
@author: HyechurnJang
'''

import boto3
from datetime import datetime, timedelta

class AWS:
    
    def __init__(self):
        self.ec2 = boto3.resource('ec2')
        self.cw = boto3.client('cloudwatch')
        
    def getVMs(self):
        aws = []
        instances = self.ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
        for instance in instances:
            desc = {
                'id' : instance.id,
                'publicIp' : instance.public_ip_address,
                'privateIp' : instance.private_ip_address,
                'hostName' : virtualMachine['hostName'],
                'metric' : {}
            }
            aws.append(desc)
        return {'amazon' : aws}
    
    def getMetric(self, vms):
        
        end = datetime.utcnow()
        start = end - timedelta(seconds=600)
        
        for vm in vms:
            try:
                
                cpu = self.cw.get_metric_statistics(
                    Period=60,
                    StartTime=start,
                    EndTime=end,
                    MetricName='CPUUtilization',
                    Namespace='AWS/EC2',
                    Statistics=['Average'],
                    Dimensions=[
                        {'Name' : 'InstanceId', 'Value' : vm['id']}
                    ]
                )
                vm['metric']['cpu'] = cpu['Datapoints'][0]['Average']
                
                net_in = self.cw.get_metric_statistics(
                    Period=60,
                    StartTime=start,
                    EndTime=end,
                    MetricName='NetworkIn',
                    Namespace='AWS/EC2',
                    Statistics=['Average'],
                    Dimensions=[
                        {'Name' : 'InstanceId', 'Value' : vm['id']}
                    ]
                )
                vm['metric']['netIn'] = net_in['Datapoints'][0]['Average']
                 
                net_out = self.cw.get_metric_statistics(
                    Period=60,
                    StartTime=start,
                    EndTime=end,
                    MetricName='NetworkOut',
                    Namespace='AWS/EC2',
                    Statistics=['Average'],
                    Dimensions=[
                        {'Name' : 'InstanceId', 'Value' : vm['id']}
                    ]
                )
                vm['metric']['netOut'] = net_out['Datapoints'][0]['Average']
                 
                disk_read = self.cw.get_metric_statistics(
                    Period=60,
                    StartTime=start,
                    EndTime=end,
                    MetricName='DiskReadBytes',
                    Namespace='AWS/EC2',
                    Statistics=['Average'],
                    Dimensions=[
                        {'Name' : 'InstanceId', 'Value' : vm['id']}
                    ]
                )
                vm['metric']['diskRead'] = disk_read['Datapoints'][0]['Average']
                 
                disk_write = self.cw.get_metric_statistics(
                    Period=60,
                    StartTime=start,
                    EndTime=end,
                    MetricName='DiskWriteBytes',
                    Namespace='AWS/EC2',
                    Statistics=['Average'],
                    Dimensions=[
                        {'Name' : 'InstanceId', 'Value' : vm['id']}
                    ]
                )
                vm['metric']['diskWrite'] = disk_write['Datapoints'][0]['Average']
        
            except Exception as e: print str(e)
