'''
Created on Jul 23, 2012

@author: autumn
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

def exec_command_alone(param_list):
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
    return (output)


#update_replace a line in a particular file
def replace_all(file1,searchExp,replaceExp):
    for line in fileinput.input(file1, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
            sys.stdout.write(line)
        

class FileNotExist(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

def __backup_file__(path):
    if os.path.isfile(path) == False:
        raise FileNotExist("File does not exist : %s" % path)
    
    bk_file = "%s.%d"
    shutil.copyfile(path, bk_file)
    return bk_file

def turn_on_flag(item):
    
    """
    Turn on rebalance flag on puppet master server in file "/etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp"
    """
    
    try:
        ring_config_file = "/etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp"
        bk_file = __backup_file__(ring_config_file)
    except Exception as e:
        #return "Error : %s" % e
        return {"retcode":-1, "output":"", "errors":"Error : %s" % e, "internval":0}
    
    try:
        f = open(ring_config_file, 'rb')
        tmp_str = f.read()
        f.close()
        
        
        if item == "rebalance":
            tmp_str = tmp_str.replace("$enforce_rebalance = 'no'", "$enforce_rebalance = 'yes'")
    
        
        if item == "remove":
            tmp_str = tmp_str.replace("$enable_node_remove = 'no'", "$enable_node_remove = 'yes'")
        
        
        f = open(ring_config_file, 'wb')
        f.write(tmp_str)
        f.close()
        os.remove(bk_file)
        
        return {"retcode":-1, "output":"OK", "errors":"", "internval":0}
    
    except Exception as e:
        cmd="cp %s %s" % (bk_file, ring_config_file)
        exec_command(cmd) 
        return {"retcode":-1, "output":"", "errors":"Error : %s" % e, "internval":0}
        
    
def turn_off_flag(item):
    """
    Turn off rebalance flag on puppet master server in file "/etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp"
    """
    try:
        ring_config_file = "/etc/puppet/modules/openstack/manifests/swift_ringbuilder.pp"
        bk_file = __backup_file__(ring_config_file)
    except Exception as e:
        return {"retcode":-1, "output":"", "errors":"Error : %s" % e, "internval":0}
    
    try:
        f = open(ring_config_file, 'rb')
        tmp_str = f.read()
        f.close()
    
        if item =="rebalance":  
            tmp_str = tmp_str.replace("$enforce_rebalance = 'yes'", "$enforce_rebalance = 'no'")
        
        if item =="remove":
            tmp_str = tmp_str.replace("$enable_node_remove = 'yes'", "$enable_node_remove = 'no'")
        
    
        f = open(ring_config_file, 'wb')
        f.write(tmp_str)
        f.close()
        os.remove(bk_file)
        
        return {"retcode":-1, "output":"OK", "errors":"", "internval":0}
    
    except Exception as e:
        cmd="cp %s %s"%(bk_file, ring_config_file)
        exec_command(cmd)
        os.remove(bk_file)
        return {"retcode":-1, "output":"", "errors":"Error : %s" % e, "internval":0}
        
    

    
   
def ring_rebalance_flag_on():   
    try:
        turn_on_flag("rebalance")
        return {"retcode":0, "output":"OK", "errors":"", "internval":0}
    except FileNotExist:
        return {"retcode":-1, "output":"", "errors":"Sorry that file does not exist", "internval":0}
  
  
def ring_rebalance_ringbuilder():
    
    try:
        cmd= "rm /etc/swift/enforce-rebalance"
        exec_command(cmd)
        cmd= "puppet agent -t"
        retcode, output, errors, interval = exec_command(cmd)
        return {"retcode":retcode, "output":output, "errors":errors, "internval":interval}
    except Exception as e:
        errors = "%s" % e 
        {"retcode": -1, "output":"", "errors":errors, "internval":0}
    #except FileNotExist:
    #    return "File does not exist : %s" % cmd

def ring_rebalance_flag_off():    
    
    try:
        turn_off_flag("rebalance")
        return {"retcode":0, "output":"OK", "errors":"", "internval":0}
    except FileNotExist:
        return {"retcode":-1, "output":"", "errors":"Sorry that file does not exist", "internval":0}
        



__proxy_node_cfg__ = """
node '%s' {
  class {'openstack::swift_base':
    swift_shared_secret => $swift_shared_secret
  }
  class { 'openstack::swift_proxy':
    swift_local_net_ip => $swift_local_net_ip,
    auth_host => $keystone_auth,
    db_host => $db_host,
  }
}
"""

__storage_node_cfg__ = """
node '%s' {
  class {'openstack::swift_base':
    swift_shared_secret => $swift_shared_secret
  }
  class {'openstack::swift_storage':
    swift_zone => %d,
    swift_local_net_ip => $swift_local_net_ip
  }
}
"""


def add_node_test(node):
    site_cfg = "/etc/puppet/manifests/site.pp"
    bk_file = __backup_file__(site_cfg)
    node_first=node.split(".")[0]
    try:
        checking=0
        for line in open(site_cfg):
                if node in line or node_first in line:
                    checking=1
                    os.remove(bk_file)
                    return {"retcode":-2,"output":"Node already exists","errors":"","interval":0}  
                    break
        if checking==0:
                os.remove(bk_file)
                return {"retcode":0, "output":"OK", "errors":"", "interval":0}
    
    
    except Exception as e:
        return {"retcode":-1, "output":"", "errors":"Error : %s" % e, "internval":0}
    
    
def add_node(node, servertype, zone=0):
    """
    Add node into /etc/puppet/manifests/site.pp 
    Param:
      node : Host name
      servertype: storagenode | proxy
    """
    try:
        site_cfg = "/etc/puppet/manifests/site.pp"
        bk_file = __backup_file__(site_cfg)
        node_first=node.split(".")[0]
        check=0
        
        if servertype == 'proxy':
            cfg = __proxy_node_cfg__ % node
        elif servertype == 'storagenode':
            cfg = __storage_node_cfg__ % (node, zone)
       
        for line in open(site_cfg):
            if node in line or node_first in line:
                check =1
                os.remove(bk_file)
                return {"retcode":-2,"output":"Node already exists","errors":"","interval":0}
                break
        
        if check==0:
            f = open(site_cfg, 'a')
            f.write(cfg)
            f.close()
            os.remove(bk_file)
            return {"retcode":0, "output":"OK", "errors":"", "internval":0}
    except Exception as e:
        return {"retcode":-1, "output":"", "errors":"Error : %s" % e, "internval":0}
    

def remove_node(node, servertype, zone=0):
    """
    Remove node from /etc/puppet/manifests/site.pp 
    Param:
      node : Host name
      servertype: storagenode | proxy
    """
    try:
        cfg = ""
        if servertype == 'proxy':
            cfg = __proxy_node_cfg__ % node
        elif servertype == 'storagenode':
            cfg = __storage_node_cfg__ % (node, zone)
        
        site_cfg = "/etc/puppet/manifests/site.pp"
        bk_file = __backup_file__(site_cfg)
        
        f = open(site_cfg, 'rb')
        tmpstr = f.read()
        f.close()
        
        tmpstr = tmpstr.replace(cfg, '')
        
        f = open(site_cfg, 'wb')
        f.write(tmpstr)
        f.close()
        
        os.remove(bk_file)  
        
        cmd = "puppet node clean node %s" % node
        retcode, output, errors, interval = exec_command(cmd) 
        return {"retcode":retcode, "output":output, "errors":errors, "interval":interval}
        #return {"output" : "OK", "tmpstr":tmpstr}
    
    except Exception as e:
        errors = "Error:%s" % e
        return {"retcode":0, "output":"", "errors":errors, "interval":0}



      
    
    
def remove_proxy_remove(node):
    
    try:
        site_cfg = "/etc/puppet/manifests/site.pp"
        bk_file = __backup_file__(site_cfg)
        cfg = __proxy_node_cfg__ % node
    
    
        f = open(site_cfg, 'rb')
        tmpstr = f.read()
        f.close()
    
        tmpstr = tmpstr.replace(cfg, '')
    
        f = open(site_cfg, 'wb')
        f.write(tmpstr)
        f.close()
        os.remove(bk_file) 
        
        return {"retcode":-1, "output":"OK", "errors":"", "internval":0}
    
    except Exception as e:
        cmd="cp %s %s"%(bk_file,site_cfg)
        exec_command(cmd)
        return {"retcode":-1, "output":"", "errors":"Error : %s" % e, "internval":0}
#    finally:
        
    

def remove_device_config(devices):
   
    remove_config_file="/etc/puppet/modules/openstack/files/remove-devices.conf"
    bk_file = __backup_file__(remove_config_file)

    device_list = devices.split(',')
    
    try:
        f = open(remove_config_file, 'a')
        #f.write(device_list)
        for line in device_list:
            if len(line) > 0:
                f.write("%s\n" % line)
        f.close()
        os.remove(bk_file)
    except Exception as e:
        cmd="cp %s %s"%(bk_file, remove_config_file)
        exec_command(cmd)
        return {"retcode":-1, "output":"", "errors":"Error : %s" % e, "internval":0}
         
    try:
        turn_on_flag("remove")
        return {"retcode":-1, "output":"OK", "errors":"", "internval":0}
    
    except FileNotExist as e:
        return {"retcode":-1, "output":"", "errors":"Error : %s" % e, "internval":0}
    
    #cmd= "puppet agent -t"
    #exec_command(cmd)       
    
    #try:
    #    turn_off_flag("remove")
    #except FileNotExist:
    #    return" sorry this file does not exist"
        

def add_device_config(devices):
    "device1, device2, ....."
    
    try:
        device_list = devices.split(',')
        
        add_config_file="/etc/puppet/modules/openstack/files/remove-devices.conf"
        bk_file = __backup_file__(add_config_file)
        
        delete_devices(add_config_file,device_list)
        os.remove(bk_file)    
    #try:
        turn_off_flag("remove")
        return {"retcode":-1, "output":"OK", "errors":"", "internval":0}
    #except FileNotExist:
    except Exception as e:
        #return "Sorry that file does not exist"
        return {"retcode":-1, "output":"", "errors":"Error : %s" % e, "internval":0}
   
    #cmd= "puppet agent -t"
    #exec_command(cmd)      
         
        
def delete_devices(file,devices):
    f=open(file,"rb")
    lines=f.readlines()
    f.close()
    f=open(file,"wb")
    for line in lines:
        #if line.strip()!=devices:
        d = line.strip()
        if devices.count(d) == 0:
            f.write(line)
    f.close()
    
def remove_ring_files():
    dir = '/etc/swift'
    rings = ['object', 'container', 'account']
    retcode = 0
    output = ""
    error = ""
    for ring in rings:
        path = "%s/%s.builder" % (dir, ring)
        try:
            os.remove(path)
            output += "removed %s\n" % path
        except Exception as e:
            retcode = -1
            error += "Error : %s\n" % e
    return {"retcode":retcode, "output":output, "errors":error, "internval":0}
        
if __name__ == '__main__':
    remove_node('ciswift006.webex.com', 'storagenode', 4)