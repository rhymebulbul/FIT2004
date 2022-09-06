import heapq


class RoadGraph:
    def __init__(self, roads, cafes):
        # ToDo: Initialize the graph data structure here
        self.positive_infinity = float('inf')
        self.pred = None
        self.dist = None
        self.pq = None
        self.V = self.get_vertices(roads)

        self.graph = [None] * self.V
        is_cafe = False
        for road in roads:
            travel_time = road[2]
            for cafe in cafes:
                if cafe[0] == road[1]:
                    travel_time += cafe[1]
                    is_cafe = True

            self.add_edge(road[0], road[1], travel_time, is_cafe)
            is_cafe = False
        self.print_graph()

    # Adds a new edge in directed graph
    def add_edge(self, src, dest, travelTime, is_cafe):
        # Adding the node to the source node
        node = AdjacencyNode(dest, travelTime, is_cafe)
        node.next = self.graph[src]
        self.graph[src] = node


    def get_vertices(self, roads):
        vertices = 0
        for road in roads:
            if road[0] > vertices:
                vertices = road[0]
            elif road[1] > vertices:
                vertices = road[1]
        vertices += 1
        return vertices


    def changeifless(self, ds, vertex, value):
        if value < ds[vertex]:
            ds[vertex] = value



    def w(self, u, v):
        temp = self.graph[u]
        while temp:
            if temp.points_to == v:
                return temp.travel_time
            #print(" -> (end:{} travel:{})".format(temp.vertex, temp.travel_time), end="")
            temp = temp.next
        pass

    def relax(self, u, v, temp):
        if self.dist[v] > self.dist[u] + self.w(u, v):
            self.dist[v] = self.dist[u] + self.w(u, v)
            self.pred[v] = u
            heapq.heappush(self.pq, (temp.travel_time, temp.points_to))

    def routing(self, start, end):
        # ToDo: Performs the operation needed to find the optimal route.
        self.pq = [(0, start)]
        self.pred = [None for _ in range(self.V)]
        self.dist = [self.positive_infinity for _ in range(self.V)]
        cafe_found = False

        print("PQ:    {} ".format(self.pq))
        print("Preced:{} ".format(self.pred))
        print("Dist:  {} ".format(self.dist))

        self.changeifless(self.dist, start, 0)
        print("Dist:  {} ".format(self.dist))

        while len(self.pq) > 0:
            priority, u = heapq.heappop(self.pq)
            temp = self.graph[u]
            while temp:
                if(temp.is_cafe):
                    cafe_found = True

                self.relax(u, temp.points_to, temp)
                temp = temp.next

        print("**********************")
        print("PQ:    {} ".format(self.pq))
        print("Preced:{} ".format(self.pred))
        print("Dist:  {} ".format(self.dist))
        print("**********************")



        route = []
        route.append(end)
        while self.pred[end] is not None:
            route.append(self.pred[end])
            end = self.pred[end]
        route.reverse()
        print(route)






    def change(self, ds, vertex, num):
        for i in range(len(ds)):
            if ds[i][num] == vertex:
                ds[i] = (vertex, num)

    def print_graph(self):
        for i in range(self.V):
            print("Adjacency list of vertex {}\n head".format(i), end="")
            temp = self.graph[i]
            while temp:
                print(" -> (end:{} travel:{} cafe: {})".format(temp.points_to, temp.travel_time, temp.is_cafe), end="")
                temp = temp.next
            print(" \n")


class AdjacencyNode:
    def __init__(self, location_id, travel_time, is_cafe):
        self.points_to = location_id
        self.travel_time = travel_time
        self.is_cafe = is_cafe
        self.next = None


if __name__ == "__main__":
    # roads = [(0, 1, 4), (0, 3, 2), (0, 2, 3), (2, 3, 2), (3, 0, 3)]
    # cafes = [(0, 5), (3, 2), (1, 3)]
    roads = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2),
             (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2),
             (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)]
    cafes = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]

    road_graph = RoadGraph(roads, cafes)
    road_graph.routing(1,3)
