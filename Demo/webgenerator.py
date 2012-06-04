'''
Created on 04.06.2012

@author: berlioz
'''
import web
import os
import urllib
import posixpath

from igraph import *

import matplotlib
matplotlib.use('Agg')

import networkx as nx
import utils  
import numpy as np
import networkx.utils as nu
import math
import matplotlib.pyplot as plt

import random as rnd

urls = (
    '/(.*)', 'index'
)

app = web.application(urls, globals())
render = web.template.render('templates/')

if not os.path.exists('generated'):
    os.mkdir('generated')
    

def RGG(n, beta, mean_degree):
    G = nx.empty_graph(n)
    powerLawArray = utils.powerLawArray(n, beta, mean_degree)
    powerLawDegreeArray = np.array(powerLawArray, dtype = np.longlong)
    sumOfDegrees = powerLawDegreeArray.sum()
    delimiterArray = np.cumsum(powerLawDegreeArray)
    delimiterArray = np.insert(delimiterArray, 0, 0)
    delimiterArray = np.delete(delimiterArray, n)
    someCounter = 0
    while someCounter < sumOfDegrees/2:
        G.add_edge(np.searchsorted(delimiterArray, rnd.randrange(sumOfDegrees)),
               np.searchsorted(delimiterArray, rnd.randrange(sumOfDegrees)))
        someCounter += 1
    txtname = "generated/adj-%s-%s-%s-.txt" % (str(n), str(beta), str(mean_degree))
    nx.write_adjlist(G, txtname)
    degreeSequence=sorted(nx.degree(G).values(),reverse=True)
    dmax=max(degreeSequence)
    plt.clf()
    plt.cla()
    plt.loglog(degreeSequence,'b-',marker='o')
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")
    if n < 1000:
        plt.axes([0.45,0.45,0.45,0.45])
        plt.cla()
        Gcc=nx.connected_component_subgraphs(G)[0]
        pos=nx.spring_layout(Gcc)
        plt.axis('off')
        nx.draw_networkx_nodes(Gcc,pos,node_size=20)
        nx.draw_networkx_edges(Gcc,pos,alpha=0.4)
    pngname = "generated/graph-%s-%s-%s-.png" % (str(n), str(beta), str(mean_degree))
    plt.savefig(pngname)
    #plt.show()
    



class index:
    def GET(self, wtf):
        inp = web.input(mean='10', power='1.7', size='10000')
        RGG(int(inp.size), float(inp.power), int(inp.mean))
        return render.index(mean=inp.mean, power=inp.power, size=inp.size)

class StaticMiddleware:
    """WSGI middleware for serving static files."""
    def __init__(self, app, prefix='/generated/',
                 root_path=r'/generated/'):
        self.app = app
        self.prefix = prefix
        self.root_path = root_path

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        path = self.normpath(path)

        if path.startswith(self.prefix):
            environ["PATH_INFO"] = os.path.join(self.root_path,
                                                web.lstrips(path, self.prefix))
            return web.httpserver.StaticApp(environ, start_response)
        else:
            return self.app(environ, start_response)

    def normpath(self, path):
        path2 = posixpath.normpath(urllib.unquote(path))
        if path.endswith("/"):
            path2 += "/"
        return path2


if __name__ == "__main__":
    wsgifunc = app.wsgifunc()
    wsgifunc = StaticMiddleware(wsgifunc)
    wsgifunc = web.httpserver.LogMiddleware(wsgifunc)
    server = web.httpserver.WSGIServer(("0.0.0.0", 8080), wsgifunc)
    print "http://%s:%d/" % ("0.0.0.0", 8080)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
