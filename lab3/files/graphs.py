import graphviz as gviz


class Graph:
    def __init__(self, edges=None, values=None):
        self._adjlist = {}
        self._valuelist = values if values is not None else {}

        if edges:
            for edge in edges:
                self.add_edge(edge[0], edge[-1])

    def __len__(self):
        return len(self._adjlist)

    def vertices(self):
        return list(self._adjlist.keys())

    def edges(self):
        eds = []
        for a in self._adjlist.keys():
            for b in self._adjlist[a]:
                if (a, b) not in eds and (b, a) not in eds:
                    eds.append((a, b))
        return eds

    def neighbours(self, v):
        return self._adjlist[v]

    def add_edge(self, a, b):
        if a not in self._adjlist:
            self._adjlist[a] = set()
        self._adjlist[a].add(b)

        if b not in self._adjlist:
            self._adjlist[b] = set()
        self._adjlist[b].add(a)

    def add_vertex(self, a):
        if a not in self._adjlist:
            self._adjlist[a] = set()

    def remove_vertex(self, v):
        if v in self._adjlist:
            del self._adjlist[v]

    def get_vertex_value(self, v):
        return self._valuelist.get(v)

    def remove_edge(self, a, b):
        if a in self._adjlist and b in self._adjlist[a]:
            self._adjlist[a].remove(b)
        if b in self._adjlist and a in self._adjlist[b]:
            self._adjlist[b].remove(a)

    def set_vertex_value(self, v, x):
        if v in self._valuelist:
            self._valuelist[v] = x


class WeightedGraph(Graph):
    def __init__(self, edges=None, weight=None):
        super().__init__(edges)
        self._weight_dict = {}

        if weight is None:
            for key in Graph.edges(self):
                self._weight_dict[key] = 1
        else:
            for stop_a in weight:
                for stop_b in weight[stop_a]:
                    self.set_weight(stop_a, stop_b, weight)

    def set_weight(self, a, b, weight=None):
        if (a, b) in self._weight_dict:
            self._weight_dict[(a, b)] = weight
        elif (b, a) in self._weight_dict:
            self._weight_dict[(b, a)] = weight
        else:
            self._weight_dict[(a, b)] = weight


    def get_weights(self, a, b):
        if (a, b) in self._weight_dict:
            v1, v2 = a, b
        elif (b, a) in self._weight_dict:
            v1, v2 = b, a
        return self._weight_dict[(v1, v2)]


def dijkstra(graph, source, cost=lambda u, v: 1):
    output, prev = {}, {}
    dist = {v: float("inf") for v in graph.vertices()}
    dist[source] = 0
    unvisited = set(graph.vertices())

    while unvisited:
        current_v = min(unvisited, key=lambda vertex: dist[vertex])

        unvisited.remove(current_v)

        for neighbor in graph.neighbours(current_v):
            weight = cost(current_v, neighbor)
            if weight is not None:
                new_dist = dist[current_v] + weight

                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = current_v

    for target in graph.vertices():
        start, path = target, []
        while start in prev:
            path.append(start)
            start = prev[start]

        path.append(source)
        path.reverse()  # Reverse the path to have it from source to target
        output[target] = {"path": path, "weight": dist[target]}
    return output



def visualize(G, view="dot", name="mygraph", nodecolors=None):
    dot = gviz.Graph(name=name, format="png")  # "neato" provides a more accurate map

    for v1 in G.vertices():
        if str(v1) in nodecolors:
            color = nodecolors.get(str(v1), "")
            dot.node(name=str(v1), color=color, style="filled")
        else:
            dot.node(str(v1))

    for v1, v2 in G.edges():
        dot.edge(str(v1), str(v2))

    dot.render(view=view, filename=name, format="png", cleanup=True)



def view_shortest(graph, source, target, cost=lambda u, v: 1):
    result_from_source = dijkstra(graph, source, cost)[target]["path"]
    result_from_target = dijkstra(graph, target, cost)[source]["path"]
    print(result_from_target)
    print(result_from_source)

    if not result_from_source or not result_from_target:
        print(f"No path found between {source} and {target}")
        return None

    path = result_from_source
    colormap = {str(v): 'orange' for v in path}
    print(colormap)

    visualize(graph, view='view', nodecolors=colormap)

# Example Usage
def demo():
    G = WeightedGraph([(1, 2), (1, 3), (1, 6), (2, 3), (2, 4), (3, 4), (3, 6), (4, 5), (5, 6)])
    print(G.vertices())
    shortest_path, node_colors = view_shortest(G, 2, 6)


if __name__ == '__main__':
    demo()

