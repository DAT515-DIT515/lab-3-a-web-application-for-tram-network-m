import json
from math import *
import os
from graphs import WeightedGraph
import django
from django.conf import settings


# path changed from lab2 version
# TODO: copy your json file from Lab 1 here

#TRAM_FILE = os.path.join(settings.BASE_DIR, 'static/tramnetwork.json')
TRAM_FILE = "/Users/andyvungoc/PycharmProjects/DAT515/lab3/static/tramnetwork.json"

# TODO: use your lab 2 class definition, but add one method
class TramStop:
    def __init__(self, name: str, lines=None, lat=None, lon=None):
        self._name = name
        self._lines = lines if lines is not None else []
        self.lat, self.lon = lat, lon
        self._position = (lat, lon)
        self.set_position(lat, lon)


    def add_line(self, line):
        if str(line) not in self._lines:
            self._lines.append(line)

    def get_line(self):
        return self._lines

    def get_name(self):
        return self._name

    def get_position(self):
        return self._position

    def set_position(self, lat, lon):
        self._position = (lat, lon)


class TramLine:
    def __init__(self, num, stops=None):
        self._number = str(num)
        self._stops = stops if stops is not None else []

    def get_number(self):
        return self._number

    def get_stops(self):
        return self._stops



class TramNetwork(WeightedGraph):
    def __init__(self, lines=None, stops=None, times=None):
        super().__init__(self)  # what does this line do?
        self._linedict = lines
        self._stopdict = stops
        self._timedict = times
        print(lines)
        print(times)
        print(times)



        for stop_name in self._stopdict.keys():
            WeightedGraph.add_vertex(self, stop_name)

        for tram_line, stops in self._linedict.items():
            for i in range(len(stops) - 1):
                    stop1 = stops[i]
                    stop2 = stops[i+1]
                    WeightedGraph.add_edge(self, stop1, stop2)
                    # WeightedGraph.set_weights(self, stop1, stop2, weight=1) # standard weight set to 1

        for stop in self._timedict:
            for neighbour in self._timedict[stop]:
                WeightedGraph.add_edge(self, stop, neighbour)
                WeightedGraph.set_weight(self, stop, neighbour, self._timedict[stop][neighbour])


    def all_lines(self):
        return self._linedict.keys()

    def all_stops(self):
        return self._stopdict.keys()

    # reuse from graphs

    def extreme_positions(self):
        lats = [self._stopdict[stop]["lat"] for stop in self._stopdict]
        lons = [self._stopdict[stop]["lon"] for stop in self._stopdict]
        minlat, minlon = min(lats), min(lons)
        maxlat, maxlon = max(lats), max(lons)
        return minlon, minlat, maxlon, maxlat

    def geo_distance(self, a, b):
        if a not in self._stopdict or b not in self._stopdict:
            return "Error: Stop not found."

        lat1, lon1 = self._stopdict[a]["lat"], self._stopdict[a]["lon"]
        lat2, lon2 = self._stopdict[b]["lat"], self._stopdict[b]["lon"]

        # convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Calculate Haversine distance
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        radius = 6371  # radius of earth in km

        return round(radius * c, 3)


    def line_stops(self, line):
        return self._linedict[line]

    def stop_lines(self, a):
        lines_v_stop = []
        for line in self._linedict:
            if a in self._linedict[line]:
                lines_v_stop.append(line)
        return lines_v_stop

    def stop_position(self, a):
        return self._stopdict[a]["lat"], self._stopdict[a]["lon"]

    def transition_time(self, a, b):
        if a in self._timedict:
            if b in self._timedict[a]:
                return self._timedict[a][b]
        if b in self._timedict:
            if a in self._timedict[b]:
                return self._timedict[b][a]



    def travel_time(self, a, b):
        time = 0
        common_line = self.stop_lines(a, b)[0]
        stops_on_line = self._linedict[common_line]
        start_index = stops_on_line.index(a)
        end_index = stops_on_line.index(b)
        if start_index == end_index:
            return time

        elif start_index < end_index:
            stops_between_values = stops_on_line[start_index: end_index + 1]
        else:
            stops_between_values = stops_on_line[end_index: start_index + 1]

        for i in range(len(stops_between_values) - 1):
            if stops_between_values[i] in self._timedict and stops_between_values[i+ 1] in self._timedict[stops_between_values[i]]:

                time += self._timedict[stops_between_values[i]
                                       ][stops_between_values[i + 1]]
            else:
                time += self._timedict[stops_between_values[i + 1]
                                       ][stops_between_values[i]]
        return time

def readTramNetwork(tramfile=TRAM_FILE):
    with open(tramfile, encoding="utf-8") as file:
        network = json.load(file)
    return TramNetwork(network["lines"], network['stops'], network['times'])

