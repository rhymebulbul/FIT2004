"""
    Monash University
    FIT2004 - Algorithms and Data Structures
    Rhyme Bulbul
    Student Number 31865224

    References:
        1. FIT2004 course notes
        2. FIT2004 week 4, 5 lecture material
        3. FIT2004 week 5, 6 studio material
        4. https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
"""

import heapq


class RoadGraph:
    """
    Class to represent road network travel times and cafe wait times in the form of an adjacency list and list
    """

    def __init__(self, roads, cafes):
        """
        Get cafes sorted into list. Iterate over roads and add as edge to graph with repective wait times
        at possible cafes and add to adjacency list to represent roads as graph
        :Input:
            roads: a list of edges, roads represented as a list of tuples (u, v, w)
            cafes: a list of locations, cafes represented as a list of tuples (location, waiting_time)
        :Postcondition: Roads are initialized as a adjacency list and cafe wait times as list
        :Time complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        :Aux space complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        """
        self.route = None
        self.type = None  # whether cafes have been visited at Node
        self.positive_infinity = float('inf')
        self.pred = None  # Stores all previous locations so we can trace back
        self.dist = None  # Stores final distances to location
        self.pq = None  # Priority Queue from heapq to implement Dijkstra's Algorithm
        self.V = self.get_vertices(roads)  # Total number of locations on graph
        self.graph = [None] * self.V  # Initialize graph to None
        self.cafes_visited = 0  # Count for number of cafes visited
        self.cafes_sorted = self.sort_cafes(cafes)  # Cafe wait times sorted by location

        for i in range(len(roads)):  # Iterate over all roads in graph
            travel_time = roads[i][2]  # Get travel time for edge/road
            src_cafe = self.cafes_sorted[roads[i][0]]  # Check wait time for source location café
            dest_cafe = self.cafes_sorted[roads[i][1]]  # Check wait time for destination location cafe
            self.add_edge(roads[i][0], roads[i][1], travel_time + src_cafe, 1)  # Add edge stopping at source
            self.add_edge(roads[i][0], roads[i][1], travel_time + dest_cafe, 2)  # Add edge stopping at destination
            self.add_edge(roads[i][0], roads[i][1], travel_time, 0)  # Add edge skipping all coffee altogether

    def get_vertices(self, roads):
        """
        Find greatest location ID to find number of vertices to form graph.
        Iterate over all road edges and location IDs to find greatest
        :Input:
            roads: a list of edges, roads represented as a list of tuples (u, v, w)
        :Output, return or postcondition: Number of vertices required to represent graph
        :Time complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        :Aux space complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        """
        vertices = 0  # Set count of vertices to zero
        for road in roads:  # Iterate over all edges
            if road[0] > vertices:  # Check if location ID is greater than current
                vertices = road[0]  # Set current location ID to greatest
            elif road[1] > vertices:  # Check if location ID is greater than current
                vertices = road[1]  # Set current location ID to greatest
        vertices += 1  # Increment by one, as we have one more vertex
        return vertices

    def sort_cafes(self, cafes):
        """
        Returns cafe wait times as list of in-place representations at each index
        Creates a list of Zeros to the size of vertices. Overwrites each cafe wait time as input cafes list is
        iterated over.
        :Input:
            cafes: a list of locations, cafes represented as a list of tuples (location, waiting_time)
        :Output, return or postcondition: a list of cafes represented as list of wait times
        :Time complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        :Aux space complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        """
        cafe_sorted = [0 for _ in range(self.V)]
        for cafe in cafes:  # Iterate over cafes and set wait times
            cafe_sorted[cafe[0]] = cafe[1]
        return cafe_sorted

    def add_edge(self, source, destination, travel_time, cafe_type):
        """
        Creates a new node to represent given edge in graph with given times. Makes use of a new Adjacency Node Class
        Object to represent a edge or path between two locations, with the source pointing to the destination
        location, along with the travel time along the edge and cafe wait times. Finally, points the source to the node.
        :Input:
            source: Source location travel is from
            destination: Destination location travel is to
            travel_time: Time to travel including wait times at any cafes
            cafe_type: Which cafes we wait at if any
        :Output, return or postcondition:
        :Time complexity: O(1), where 'V' is number of vertices and 'E' is number of edges in graph
        :Aux space complexity: O(1), where 'V' is number of vertices and 'E' is number of edges in graph
        """
        # Create Adjacency Node
        node = AdjacencyNode(destination, travel_time, cafe_type)
        # Point adjacency nodes from source and to next
        node.next = self.graph[source]
        self.graph[source] = node

    def delete_edge(self, source, destination):
        """
        Iterates over all edges from source vertex till destination is reached and deletes edge
        Takes in soure node and checks all neighbouring edges for destination nodes as well as types.
        :Input:
            source: Source location of edge to delete from
            destination: Destination location of edge to delete to
        :Output, return or postcondition: Target edge from source to destination is deleted
        :Time complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        :Aux space complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        """
        temp = self.graph[source]  # Set graph to source vertex
        while temp:  # Iterate over all edges from source vertex till destination is found
            if temp.points_to == destination and 0 <= temp.travel_type < 4:
                temp.travel_time = self.positive_infinity  # Delete edge by setting travel time to infinity
            temp = temp.next  # move to next edge in graph

    def w(self, u, v):
        """
        Iterates over adjacency list node u, till node v is found and then returns time as weight of edge
        Moves to node u in the graph and checks each neighbouring edge, stores and compares to get least weight.
        :Input:
            u: starting location
            v: end location
        :Output, return or postcondition: Weight of edge from u to v in time of travel including cafe wait times
        :Time complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        :Aux space complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        """
        temp = self.graph[u]  # Set graph to start node u
        final = 0, self.positive_infinity
        time = self.positive_infinity
        while temp:  # Iterate over all edges from node u
            if temp.points_to == v:  # If end node v is found
                if temp.travel_time <= time:  # and weight in time is less than current
                    time = temp.travel_time  # Update current least time
                    final = temp.travel_time, temp.travel_type  # Update current least time and type
            temp = temp.next  # Iterate to next edge
        return final  # Return least

    def relax(self, u, v, node):
        """
        Maintains for each vertex, the length of the shortest path to that vertex that we have found so far.
        If distance to the node v is less than what we have stored currently, we update distance, update
        predecessor list.
        :Input:
            u: start location
            v: end location
            temp: graph node we are currently at
        :Output, return or postcondition:
        :Time complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        :Aux space complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        """
        if self.dist[v] > self.dist[u] + self.w(u, v)[0]:  # Check if distance is less
            self.dist[v] = self.dist[u] + self.w(u, v)[0]  # Update distance
            self.pred[v] = u  # Set predecessor node to trace back
            self.type[v] = self.w(u, v)[1]  # Set cafe we stopped at if we did
            heapq.heappush(self.pq, (node.travel_time, node.points_to))  # Push priority and node to min heap

    def dijkstra(self, start, end):
        """
        Implements a version of Dijkstra's Algorithm using min heap as priority queue
        Finally uses predecessor array to find the shortest route to end location only
        Takes start element and relaxes all neighbouring edges. Rinse and repeat till priority queue is empty.
        Find the route of this shortest path with get_route().
        :Input:
            start: start location
            end: end location
        :Output, return or postcondition: Returns shortest route to end node only
        :Time complexity: O(Elog(V)), where 'V' is number of vertices and 'E' is number of edges in graph
        :Aux space complexity: O(V + E), where 'V' is number of vertices and 'E' is number of edges in graph
        """
        self.pq = [(0, start)]  # Priority Queue
        self.pred = [None for _ in range(self.V)]  # Predecessor List  [float("Inf")] * self.V
        self.dist = [float("Inf")] * self.V  # Final Distance List
        self.type = [float("Inf")] * self.V  # cafe type list
        self.dist[start] = 0  # Set start location to highest priority or, zero
        while len(self.pq) > 0:  # Pop off minimum item of priority queue until its empty
            priority, u = heapq.heappop(self.pq)  # Store item
            temp = self.graph[u]  # Get graph vertex of item
            while temp:  # while vertex has neighbouring edges, relax each
                self.relax(u, temp.points_to, temp)
                temp = temp.next  # Jump to next neighbour
        return self.get_route(end)  # Get route to end location and return

    def get_route(self, end):
        """
        Back tracks locations starting from the end in the predecessor array and adds each to a list of locations,
        which forms the route of locations. Starts from end and back tracks predecessor list, adding each location
        on the way. Finally we reverse the list to get the right order.
        :Input:
            end: end location
        :Output, return or postcondition: List of locations to visit to form shortest path
        :Time complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        :Aux space complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        """
        self.cafes_visited = 0  # Set visited cafes to zero
        temp = end
        route = [temp]  # Set route to end
        if self.cafes_sorted[temp] > 0:
            self.cafes_visited += 1
        while self.pred[temp] is not None:  # Iterate predecessor list to find path
            if self.cafes_sorted[self.pred[temp]] > 0:  # Check if cafe was visited
                self.cafes_visited += 1  # Increment cafe count
            route.append(self.pred[temp])  # Append path to route list from predecessor array
            temp = self.pred[temp]  # update temp end
        route.reverse()  # Reverse list to get right order
        return route

    def routing(self, start, end):
        """
        Runs Dijkstra's algorithm until one cafe is found along the shortest path
        First run of Dijkstra's Algorithm will return the shortest path, evidently with no cafe wait times. Removing
        one edge and re-running Dijkstra, we get the second shortest path, which must contain the cafe with the least
        wait time. Rinse and repeat till at least one cafe is found.
        :Input:
            start: start location
            end: end location
        :Output, return or postcondition: Shortest path to grab a coffee
        :Time complexity: O(Elog(V)), where 'V' is number of vertices and 'E' is number of edges in graph
        :Aux space complexity: O(V + E), where 'V' is number of vertices and 'E' is number of edges in graph
        """
        self.route = [start, end]  # Route holding start and end
        prev = self.route  # Copy of route
        self.route = self.dijkstra(start, end)  # run dijkstra's algorithm
        # temp = self.graph[self.route[0]]
        # while len(self.route) == 1:
        #     # if start == end:  # Re-run same start and end locations
        #     print("equial: ")
        #     print(self.route)
        #
        #     print(start)
        #     print(temp.points_to)
        #     self.delete_edge(start, temp.points_to)  # Delete edge
        #     self.route = self.dijkstra(start, end)  # Re-run dijkstra's algorithm
        #     temp.next

        while self.cafes_visited < 1:  # Re-run until at least one cafe is found
            if len(self.route) < len(prev):  # If the path found is even shorter, a cycle is needed.
                self.delete_edge(prev[1], prev[0])  # Delete edge from path
                self.route = self.dijkstra(end, start)  # Re-run dijkstra's algorithm
                temp = []  # Holds part of cyclic path
                for i in range(len(prev)):  # Add first part
                    temp.append(prev[i])
                for i in range(1, len(self.route) - 1):  # Add coffee run
                    temp.append(self.route[i])
                for i in range(len(prev)):  # Add last run back to destination
                    temp.append(prev[i])
                # if self.cycle(self.route):
                #     return None
                return temp  # Return the path
            else:  # Continue otherwise
                self.delete_edge(self.route[0], self.route[1])  # Delete edge
                prev = self.route  # Update prev variable
                self.route = self.dijkstra(start, end)  # Re-run dijkstra's algorithm
                if len(self.route) >= 2:
                    self.delete_edge(self.route[0], self.route[1])  # Delete edge
                    prev = self.route  # Update prev variable
                    self.route = self.dijkstra(start, end)  # Re-run dijkstra's algorithm
                #elif len(self.route) == 1:


        if self.cycle(self.route):
            return None
        return self.route

    def cycle(self, path):
        """
        Tells us if we walked a cycle.
        A cycle would be walked if we repeat the same path twice in the route only. As such, we iterate from both the
        start to mid; and mid to end of the route list, while comparing elements. Any elements that do not match
        confirm the lack of a cycle. If all elements match a cycle is confirmed.
        :Input:
            path: route to test
        :Output, return or postcondition: whether a cycle exists has been discovered
        :Time complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        :Aux space complexity: O(V), where 'V' is number of vertices and 'E' is number of edges in graph
        """
        mid = len(path) // 2  # Find middle
        for i in range(mid):  # Iterate over route til mid
            if path[i] != path[i + mid]:  # Check if the same location is repeated in cycle
                return False
        return True


class AdjacencyNode:
    def __init__(self, location_id, travel_time, travel_type):
        """
        Represents one edge in Adjacency graph, as well as travel time, including wait time if one location is a cafe
        Uses the basic linked list structure to represent an adjacency list with each node representing a location
        and additional data in the node such as the wait time of any cafes, as well as the next location this path
        leads to, in the form of a next node.
        :Input:
            location_id: Location ID of destination
            travel_time: Time to travel to destination, including any time spent waiting at a cafe
            travel_type: Which cafe we stopped at if we did
        :Output, return or postcondition: Graph edge is initialised with required data
        :Time complexity: O(1), where 'V' is number of vertices and 'E' is number of edges in graph
        :Aux space complexity: O(1), where 'V' is number of vertices and 'E' is number of edges in graph
        """
        self.points_to = location_id
        self.travel_time = travel_time
        self.travel_type = travel_type
        self.next = None

class Graph:

    def __init__(self, vertices):
        self.V = vertices  # Total number of vertices in the graph
        self.graph = []  # Array of edges

    # Add edges
    def addEdge(self, s, d, w):
        self.graph.append([s, d, w])

    # Print the solution
    def print_solution(self, dist):
        print("Vertex Distance from Source")
        for i in range(self.V):
            print("{0}\t\t{1}".format(i, dist[i]))

    def BellmanFord(self, src, end):
        pred = [None] * self.V
        # Step 1: fill the distance array and predecessor array
        dist = [float("Inf")] * self.V
        # Mark the source vertex
        dist[src] = 0

        # Step 2: relax edges |V| - 1 times
        for _ in range(self.V - 1):
            for s, d, w in self.graph:
                if dist[s] != float("Inf") and dist[s] + w < dist[d]:
                    dist[d] = dist[s] + w
                    pred[d] = s

        # Step 3: detect negative cycle
        # if value changes then we have a negative cycle in the graph
        # and we cannot find the shortest distances
        for s, d, w in self.graph:
            if dist[s] != float("Inf") and dist[s] + w < dist[d]:
                print("Graph contains negative weight cycle")
                return

        # No negative weight cycle found!
        # Print the distance and predecessor array
        #self.print_solution(dist)

        #print(pred)
        temp = end
        route = [temp]  # Set route to end

        while pred[temp] is not None:  # Iterate predecessor list to find path

            route.append(pred[temp])  # Append path to route list from predecessor array
            temp = pred[temp]  # update temp end
        route.reverse()  # Reverse list to get right order
        #print(route)
        return route

def optimalRoute(downhillScores, start, finish):
    g = Graph(7)
    for trail in downhillScores:
        g.addEdge(trail[0], trail[1], -trail[2])
    # # function call
    return g.BellmanFord(start, finish)

# if __name__ == "__main__":
    # roads = [(0, 1, 4), (0, 3, 2), (0, 2, 3), (2, 3, 2), (3, 0, 3)]
    # cafes = [(0, 5), (3, 2), (1, 3)]
    # roads = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 4, 1), (1, 5, 2),
    #          (5, 6, 5), (6, 3, 2), (6, 4, 3), (1, 7, 4), (7, 8, 2),
    #          (8, 7, 2), (7, 3, 2), (8, 0, 11), (4, 3, 1), (4, 8, 10)
    #     , (5, 9, 1), (9, 10, 2), (10, 11, 3), (11, 12, 1)]
    # cafes = [(5, 10), (6, 1), (7, 5), (0, 3), (8, 4)]
    #
    # road_graph = RoadGraph(roads, cafes)
    #
    # print(road_graph.routing(1,1))
    # Example
    # The scores you can obtain in each downhill segment
    # downhillScores = [(0, 6, -500), (1, 4, 100), (1, 2, 300),
    #                   (6, 3, -100), (6, 1, 200), (3, 4, 400), (3, 1, 400),
    #                   (5, 6, 700), (5, 1, 1000), (4, 2, 100)]
    # # The starting and finishing points
    # start = 6
    # finish = 2
    # print(optimalRoute(downhillScores, start, finish))
    # print([6, 3, 1, 2])