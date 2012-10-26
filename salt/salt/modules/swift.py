'''
Created on Jul 25, 2012

@author: autumn
'''

import os
import time
import ConfigParser
import subprocess as sub

def __exec_command__(param_list):
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
    #print "cmd = %s, output = %s" % (param_list[0], output)
    return (p.returncode, output, errors, interval)

def __get_services__():
    ret = []
    for s in os.listdir("/etc/init.d"):
        if s.startswith('swift-'):
            ret.append(s)
    return ret

def service_status():
    ret = {}
    services = __get_services__()
    _output = ''
    for s in services:
        cmd = "service %s status" % s
        (retcode, output, errors, interval) = __exec_command__([cmd])
        print "retcode=%d, output=%s" % (retcode, output)
        tmplist = output.split(" ", 1)
        if len(tmplist) > 1:
            status = tmplist[1].strip()
            #ret[s] = status
            _output += "%30s : %-20s\n" % (s, status)
        else:
            _output += "%s:%s\n" % (s,'unknown')
    ret['retcode'] = 0
    ret['output'] = _output
    ret['errors'] = ''
    ret['servertype'] = __salt__['grains.item']('servertype')
    return ret

def get_cluster_infor():
    config = ConfigParser.RawConfigParser()
    cfg_file = "/etc/swift/swift.conf"
    config.read(cfg_file)
    ret = {}
    ret['name'] = config.get("default", "cluster")
    ret['hashkey'] = config.get("swift-hash", "swift_hash_path_suffix")
    return ret

def ring_infor():
    cmd = 'swift-ring-builder '

##################################################
##
if __name__ == '__main__':
    ret = service_status()
    print "%r" % ret