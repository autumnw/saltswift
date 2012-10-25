# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse


def test(request):
    t = loader.get_template('server/test.html')
    c = Context({
    })
    return HttpResponse(t.render(c))

def serverdetails(request, host):
    server_info = dict()
    server_info['Host'] = host
    server_info['IP address'] = '10.100.18.125'
    server_info['Service.swift-proxy'] = 'Active'
    server_info['Service.swift-object'] = 'Active'
    t = loader.get_template('server/detail.html')
    c = Context({
        'server_info': server_info, 'host':host
    })
    return HttpResponse(t.render(c))

