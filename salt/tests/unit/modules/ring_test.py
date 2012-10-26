import unittest

import os.path
import os
import sys
import shutil
import fileinput
import time
import subprocess as sub
from salt.modules.ring import *


class TestRing(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_add_node(self):
        
        path = "/etc/puppet/manifests"
        file = 'site.pp'
        if os.path.exists(path) == False:
            os.makedirs(path, 0777)
        
        obspath = os.sep.join([path, file])
        
        if os.path.exists(obspath):
            os.remove(obspath)
        f = open(obspath, 'wb')
        f.close()
        
        node  = 'ciswift001.webex.com'
        servertype = 'proxy'
        
        ret = add_node(node, servertype, zone=0) 
        result = ret['retcode']
        expected = 0
        
        print "result = %r" % result
        
        self.assertEquals(result, expected)
        
    
  
    def test_remove_node(self):
        
        path = "/etc/puppet/manifests"
        file = 'site.pp'
        if os.path.exists(path) == False:
            os.makedirs(path, 0777)
        
        obspath = os.sep.join([path, file])
        
        if os.path.exists(obspath):
            os.remove(obspath)
        f = open(obspath, 'wb')
        f.close()
        
        node  = 'ciswift001.webex.com'
        servertype = 'proxy'
        
        ret = remove_node(node, servertype, zone=0)
        result = ret['retcode']
        
        cmd = "puppet node clean node %s" % node
        (expected,a,b,c) = exec_command(cmd)
        
        print "result = %r" % result
        
        self.assertEquals(result, expected) 