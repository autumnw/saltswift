'''
Created on Aug 10, 2012

@author: xiaomeli
'''
import os
import sys
import shutil
import fileinput
import time
import subprocess as sub


def exec_command(param_list):
    """
    Execute a command:
      @param param_list: ['cmd param1 param2']
    """
    s_time = time.time()
    p = sub.Popen(param_list, stdout = sub.PIPE, stderr = sub.PIPE, shell=True)
    output, errors = p.communicate()
    p.wait()
    e_time  = time.time()
    interval = e_time - s_time
    return (p.returncode, output, errors, interval)



def nodetest_preverification(storage_server,account_server_port,container_server_port,object_server_port,device):
    try:
        cmd= "swift-pre-verification %s %s %s %s %s" % (storage_server,account_server_port,container_server_port,object_server_port,device)
        #exec_command(cmd)
        #cmd= "swift-console pre-node-test -s ciswift008.webex.com preverification"
        retcode, output, errors, interval = exec_command(cmd)
        return {"retcode":retcode, "output":output, "errors":errors, "internval":interval}
    except Exception as e:
        errors = "%s" % e 
        return {"retcode": -1, "output":"", "errors":errors, "internval":0}
    
        
        
def nodetest_postverfication(identity_url,storage_server,user,password,tenent,container):        
    try:
        cmd= "swift-post-verification %s %s %s %s %s" % (identity_url,storage_server,user,password,tenent,container)
        #exec_command(cmd)
        #cmd= "swift-console post-node-test -s ciswift008.webex.com postverification"
        retcode, output, errors, interval = exec_command(cmd)
        return {"retcode":retcode, "output":output, "errors":errors, "internval":interval}
    except Exception as e:
        errors = "%s" % e 
        return {"retcode": -1, "output":"", "errors":errors, "internval":0}