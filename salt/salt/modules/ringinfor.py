'''
Created on Jul 18, 2012

@author: autumn
'''

#from swiftconsole.common.utils import exec_command

import time
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
    return (p.returncode, output, errors, interval)


def __get_ring_info__(ring):
    cmd = "swift-ring-builder /etc/swift/%s.builder" % ring
    retcode, output, errors, interval = __exec_command__([cmd])
    
    ret = dict()
    ret['retcode'] = retcode
    ret['output'] = output
    ret['errors'] = errors
    ret['interval'] = interval
    
    return ret

def account_ring():
    return __get_ring_info__('account')

def container_ring():
    return __get_ring_info__('container')

def object_ring():
    return __get_ring_info__('object')


############################
## For testing
if __name__ == '__main__':
    (retcode, output, errors, interval) = account_ring()
    print "[%d] %s" % (retcode, '\n'.join([output, errors]))
    
    

