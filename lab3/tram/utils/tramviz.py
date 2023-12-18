from .trams import readTramNetwork #, specialized_transition_time, specialized_geo_distance, specialize_stops_to_lines
from .graphs import dijkstra
from .color_tram_svg import color_svg_network
import os
from django.conf import settings


def show_shortest(dep, dest):
    # TODO: uncomment this when it works with your own code
    network = readTramNetwork()
    # TODO: replace this mock-up with actual computation using dijkstra.
    # First you need to calculate the shortest and quickest paths, by using appropriate
    # cost functions in dijkstra().
    # Then you just need to use the lists of stops returned by dijkstra()
    # If you do Bonus 1, you could also tell which tram lines you use and where changes
    # happen. But since this was not mentioned in lab3.md, it is not compulsory.

    quickest = dijkstra(network, dep, cost=lambda u,v: network.transition_time(u,v))[dest]
    print("Quickest"+ str(quickest))
    shortest = dijkstra(network, dep, cost=lambda u,v: network.geo_distance(u,v))[dest]
    print("Shortest"+str(shortest))

    timepath = f'Quickest: {" - ".join(quickest["path"])}, {quickest["weight"]} minutes'
    geopath = f'Shortest:  {" - ".join(shortest["path"])}, {round(shortest["weight"], 2)} km'
    #print(specialize_stops_to_lines(network))
    #print(specialized_transition_time(specialize_stops_to_lines(network)))
    def colors(v):
        if (v in shortest['path']) and (v in quickest['path']):
            return 'cyan'
        elif v in shortest['path']:
            return 'lightgreen'
        elif v in quickest['path']:
            return 'orange'
        else:
            return 'white'

    # this part should be left as it is:
    # change the SVG image with your shortest path colors
    color_svg_network(colormap=colors)
    # return the path texts to be shown in the web page
    return timepath, geopath


