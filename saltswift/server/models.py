import os
import socket

from django.db import models
from salt.client import LocalClient

STATUS_DICT = {True:"Accessible", False:"Inaccessible"}

salt_client = LocalClient()

# Create your models here.
class Server(models.Model):
    ip = models.IPAddressField()
    hostname = models.CharField(max_length=200)
    status = models.IntegerField()
    #pub_date = models.DateTimeField('date published')


def __get_server_status__(host):
    result = salt_client.cmd(host, "test.ping")
    return STATUS_DICT[result[host]]

def get_server_list():
    ret = list()
    server_list = salt_client.cmd("*", "grains.item", ["servertype"])
    
    for (server, type) in server_list.iteritems():
        ip = socket.gethostbyname(server)
        status = __get_server_status__(server)
        
        the_type = type
        if isinstance(type,list):
            the_type = ' / '.join(the_type)
        ret.append((server, ip, status, the_type))
        
    return ret
        
