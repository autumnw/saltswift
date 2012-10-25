from django.template import Context, loader
from django.http import HttpResponse
import server.models as server_model
import cluster.models as cluster_model

def index(request):
    return server(request)

def server(request):
    server_list = server_model.get_server_list()
    print "%r" % server_list
    t = loader.get_template('server/index.html')
    c = Context({
        'server_list': server_list,
    })
    return HttpResponse(t.render(c))

def cluster(request):
    server_list = server_model.get_server_list()
    host = None
    for (server, ip, status, the_type) in server_list:
        if status == 'Accessible':
            host = server
            break
        
    #print "host = %s" % host
    
    cluster_infor = cluster_model.get_cluster_infor(host)
    
    #print "cluster_infor = %r" % cluster_infor
    
    t = loader.get_template('cluster/index.html')
    c = Context({'cluster_infor': cluster_infor})
    return HttpResponse(t.render(c))

def monitor(request):
    t = loader.get_template('monitor/index.html')
    c = Context({})
    return HttpResponse(t.render(c))
