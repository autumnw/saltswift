from django.db import models
from salt.client import LocalClient
# Create your models here.

salt_client = LocalClient()

def ring_infor():
    args = ['servertype:swift-ringbuilder', 'swift.volumes', [], 5, 'grain', '']
    

def storage_infor():
    """''servertype:swift-storagenode', 'test.ping', [],5, 'grain', ''"""
    args = ['servertype:swift-storagenode', 'swift.volumes', [], 5, 'grain', '']
    result = salt_client.cmd(*args)
    ret = {}
    total_size = 0
    used_size = 0
    for key, value in result.iteritems():
        total_size += value['total_size_1k']
        used_size += value['used_size_1k']
    ret['total_size'] = total_size
    ret['used_size'] = used_size
    ret['used_percent'] = float(used_size)/total_size
    ret['details'] = result

def get_cluster_infor(host):
    result = salt_client.cmd(host, "swift.get_cluster_infor")
    ret = dict(result[host])
    