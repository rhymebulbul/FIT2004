

# Class to represent a graph
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
        self.print_solution(dist)

        print(pred)
        temp = end
        route = [temp]  # Set route to end

        while pred[temp] is not None:  # Iterate predecessor list to find path

            route.append(pred[temp])  # Append path to route list from predecessor array
            temp = pred[temp]  # update temp end
        route.reverse()  # Reverse list to get right order
        print(route)



# Driver's code
if __name__ == '__main__':
    # g = Graph(5)
    # g.addEdge(0, 1, -1)
    # g.addEdge(0, 2, 4)
    # g.addEdge(1, 2, 3)
    # g.addEdge(1, 3, 2)
    # g.addEdge(1, 4, 2)
    # g.addEdge(3, 2, 5)
    # g.addEdge(3, 1, 1)
    # g.addEdge(4, 3, -3)
    # g.BellmanFord(0)
    #
    g = Graph(7)
    downhillScores = [(0, 6, -500), (1, 4, 100), (1, 2, 300),
                      (6, 3, -100), (6, 1, 200), (3, 4, 400), (3, 1, 400),
                      (5, 6, 700), (5, 1, 1000), (4, 2, 100)]
    downhillScores.sort()
    for trail in downhillScores:
        g.addEdge(trail[0], trail[1], -trail[2])
    #
    # # function call
    g.BellmanFord(6, 2)

