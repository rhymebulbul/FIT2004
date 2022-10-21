"""
Monash University
FIT2004 - Algorithms and Data Structures
Assignment 3

Rhyme Bulbul
31865224

References:
    1. Wikimedia Foundation. (2022, August 4). Flow network. Wikipedia. Retrieved October 19, 2022, from https://en.wikipedia.org/wiki/Flow_network
    2. Wikimedia Foundation. (2022, October 13). Ford–Fulkerson algorithm. Wikipedia. Retrieved October 19, 2022, from https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm
    3. Wikimedia Foundation. (2021, December 4). Circulation problem. Wikipedia. Retrieved October 19, 2022, from https://en.wikipedia.org/wiki/Circulation_problem
    4. Faculty of Information Technology, Monash University. (2022, September). Lecture 8 - Network Flow. FIT2004: Algorithms and Data Structures. Melbourne.
    5. Faculty of Information Technology, Monash University. (2022, September). Lecture 9 - Circulation with Demands and Applications of Network Flow. FIT2004: Algorithms and Data Structures. Melbourne.
    6. Wikimedia Foundation. (2022, August 9). Suffix Tree. Wikipedia. Retrieved October 19, 2022, from https://en.wikipedia.org/wiki/Suffix_tree
    7. Wikimedia Foundation. (2022, March 11). Generalized suffix tree. Wikipedia. Retrieved October 19, 2022, from https://en.wikipedia.org/wiki/Generalized_suffix_tree
    8. Wikimedia Foundation. (2022, June 3). Longest common substring problem. Wikipedia. Retrieved October 19, 2022, from https://en.wikipedia.org/wiki/Longest_common_substring_problem
    9. Faculty of Information Technology, Monash University. (2022, October). Lecture 11 - Retrieval Data Structures for Strings. FIT2004: Algorithms and Data Structures. Melbourne.
"""

import math
from typing import Optional


class Transformer:

    def __init__(self, availabilities: list) -> None:
        """
        Class that initializes graph of appropriate size for availabilities, models the graph, adds edges as required,
        deletes super source and sink when fit and turns matches into meals roster
        :Input:
            availabilities: list of list representing availability of each person by day
        :Output, return or postcondition: Graph is initialized with all relevant parameters
        :Time complexity: O(n2), where n is the number of next days to allocate meal prep for
        :Aux space complexity: O(n2), where n is the number of next days to allocate meal prep for
        """
        self.availability = availabilities
        self.number_of_days = len(availabilities)
        self.number_of_people = len(availabilities[0])
        self.min_meal = math.floor(0.36 * self.number_of_days)
        self.max_meal = math.ceil(0.44 * self.number_of_days)
        self.max_takeaway = math.floor(0.1 * self.number_of_days)
        self.demand = 2 * self.number_of_days
        self.source_demand = -self.demand
        self.sink_demand = self.demand
        self.flow_max = 0
        self.size = self.counter()
        self.super_graph = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.person_to_selector = [[] for _ in range(self.number_of_people)]

    def counter(self) -> int:
        """
        Counts one node each for super source and sink, orgins of allocations and verified and restaurants
        and then one for each person and one for each meal. Then counts one for each selector node a person
        is available
        :Input: None
        :Output, return or postcondition: Size of graph
        :Time complexity: O(n2), where n is the number of next days to allocate meal prep for
        :Aux space complexity: O(n2), where n is the number of next days to allocate meal prep for
        """
        count = 3 + self.number_of_people + 2 * self.number_of_days + 2
        for i in range(self.number_of_days):  # Each day
            for j in range(len(self.availability[i])):  # Each person
                if self.availability[i][j] > 0:  # if person is available, selector is required
                    count += 1
        return count

    def transform_graph(self) -> list:
        """
        Models a graph for network flow from origin of allocations to person, to selector node, to meal, to
        allocations verified, as well as origin to restaurant to meal to origin. Adds in super source and
        sink nodes in accordance with demands and lower bounds. Keeps track of each person and meals their
        selector nodes connect
        :Input: None
        :Output, return or postcondition: Circulation graph with demands and lower bounds set
        :Time complexity: O(n2), where n is the number of next days to allocate meal prep for
        :Aux space complexity: O(n2), where n is the number of next days to allocate meal prep for
        """
        origin_allocations = 0  # Set first to origin of allocations
        restaurant = 1  # Set next to restaurant
        allocations_verified = self.size - 3  # Set third last to verified allocations
        super_source = self.size - 2  # Set second last to super source
        super_sink = self.size - 1  # Set last to super sink

        # Add origin of allocations -> restaurant
        self.add_edge(self.super_graph, origin_allocations, restaurant, self.max_takeaway)

        # Add super source -> origin of allocations: Set max flow as demanded
        self.add_edge(self.super_graph, super_source, origin_allocations, self.demand - self.min_meal)

        # Add source -> each person
        people_start = 2
        for person in range(people_start, people_start + self.number_of_people):
            # Add origin of allocations -> each person
            self.add_edge(self.super_graph, origin_allocations, person, self.max_meal - self.min_meal)  # max-min
            # Add super source -> each person
            self.add_edge(self.super_graph, super_source, person, self.min_meal)

        edge_count = people_start + self.number_of_people  # Counts edges iterated to add in selector node

        for i in range(self.number_of_days):  # Each day
            breakfast_head = edge_count  # First person of day, mark meal
            dinner_head = breakfast_head + 1
            edge_count += 2  # Counts edges iterated to add in meal heads

            # Add restaurant -> breakfast
            self.add_edge(self.super_graph, restaurant, breakfast_head)
            # Add restaurant -> Dinner
            self.add_edge(self.super_graph, restaurant, dinner_head)

            # Add meal to super sink
            self.add_edge(self.super_graph, breakfast_head, super_sink)
            self.add_edge(self.super_graph, dinner_head, super_sink)

            for j in range(len(self.availability[i])):  # Each person
                person = j + 2  # Person
                if self.availability[i][j] > 0:
                    selector = edge_count  # Create selector node
                    edge_count += 1  # Counts edges iterated to add in meal heads

                    # Add person -> selector
                    self.add_edge(self.super_graph, person, selector)

                    if self.availability[i][j] == 1 or self.availability[i][j] == 3:  # Breakfast
                        self.add_edge(self.super_graph, selector, breakfast_head)  # Add selector -> breakfast

                    if self.availability[i][j] == 2 or self.availability[i][j] == 3:  # Dinner
                        self.add_edge(self.super_graph, selector, dinner_head)  # Add selector -> Dinner

                    # person -> [selector, breakfast, dinner, day]
                    self.person_to_selector[j].append([selector, breakfast_head, dinner_head, i])

        # allocations_verified -> super_sink
        self.add_edge(self.super_graph, allocations_verified, super_sink, self.sink_demand - 1)

        return self.super_graph

    def add_edge(self, graph: list, vertex_from: int, vertex_to: int, capacity=1) -> None:
        """
        Adds in edge between from and to vertices in given graph, setting capacity if specified, otherwise
        defaulting to none
        :Input:
            graph:  Network flow graph to add edges in
            vertex_from: start vertex
            vertex_to: end vertex
            capacity: Edge flow maximum capacity to set to
        :Output, return or postcondition: Edge has been added in graph
        :Time complexity: O(1), where n is the number of next days to allocate meal prep for
        :Aux space complexity: O(1), where n is the number of next days to allocate meal prep for
        """
        graph[vertex_from][vertex_to] = capacity

    def delete_super(self, super_graph: list) -> list:
        """
        Removes the super sink and super source from the end of the graph, as they are no longer required
        after the max flow has been found
        :Input:
            super_graph:  Network flow graph to add edges in
        :Output, return or postcondition: graph with super source and sink omitted
        :Time complexity: O(n2), where n is the number of next days to allocate meal prep for
        :Aux space complexity: O(n2), where n is the number of next days to allocate meal prep for
        """
        # final graph omitting super source and super sink, which are last two nodes
        final = [[super_graph[i][j] for i in range(len(super_graph) - 2)] for j in range(len(super_graph) - 2)]
        return final

    def get_results(self, final: list) -> tuple:
        """
        Iterates the selector node data, and checks if a path exists from person to selector to meal.
        Allocate person  within constraints to available meal prep if exists, otherwise check if takeaway can be ordered
        :Input:
            final: Network flow graph to add edges in
        :Output, return or postcondition: tuple containing allocated people for breakfast and dinner
        :Time complexity: O(n), where n is the number of next days to allocate meal prep for
        :Aux space complexity: O(n), where n is the number of next days to allocate meal prep for
        """
        breakfast = [-1 for _ in range(self.number_of_days)]
        dinner = [-1 for _ in range(self.number_of_days)]
        restaurant = 1    # Denotes node restaurant is located at
        # person -> [selector, breakfast, dinner]
        for person in range(len(self.person_to_selector)):
            selector_person = self.person_to_selector[person]
            for meal in selector_person:
                selector_index = meal[0]
                breakfast_index = meal[1]
                dinner_index = meal[2]
                day = meal[3]
                if final[person + 2][selector_index] == 1 and final[selector_index][breakfast_index] == 1:
                    breakfast[day] = person   # Person allocated to breakfast
                if final[person + 2][selector_index] == 1 and final[selector_index][dinner_index] == 1:
                    dinner[day] = person    # Person allocated to dinner
                if final[restaurant][breakfast_index] == 1:
                    breakfast[day] = 5     # Takeaway breakfast
                if final[restaurant][dinner_index] == 1:
                    dinner[day] = 5     # Takeaway dinner
        return (breakfast, dinner)


def allocate(availability: list) -> Optional[tuple]:
    """
    Initializes a transformer object based on everyones availability. Models the network graph based on
    circulations and demands with lower bounds, and then solves using Ford Fulkerson to find the max flow.
    Will return none if not feasible, otherwise, a roster of allocated meal prep persons
    :Input:
        availability: times each person is available to take on meal prep
    :Output, return or postcondition: Each person is allocated within constraints
    :Time complexity: O(n2), where n is the number of next days to allocate meal prep for
    :Aux space complexity: O(n2), where n is the number of next days to allocate meal prep for
    """
    transformer = Transformer(availability)
    # Create the supergraph G' from G
    super_graph = transformer.transform_graph()
    # return unfeasible if sink and source do not have the same demand
    if transformer.source_demand + transformer.sink_demand != 0:
        return None
    # Solve the max-flow problem in supergraph using Ford Fulkerson to obtain max flow
    flow_max = ford_fulkerson(super_graph, transformer.size - 2, transformer.size - 1)
    # Not feasible if max flow is not equal to demand in either source or sink
    if abs(flow_max) != transformer.sink_demand:
        return None
    # Given max flow in super graph, delete super source and super sink to obtain flow
    final = transformer.delete_super(super_graph)
    # Allocate meal prep within constraints
    return transformer.get_results(final)


def bread_first_search(graph: list, source: int, sink: int, parent_graph: list) -> bool:
    """
    Creates a queue for nodes to service, adds source. Creates list for already visited nodes, marks off source
    as visited. Pops first ready node of queue and visits all of its immediate neighbours. If neighbours haven't
    been visited, marks of as visited and appends to queue
    :Input:
        graph:  Network flow graph to search breadth-first
        source:  Source node to start from
        sink:   Sink node to end at
        parent_graph: parent graph
    :Output, return or postcondition:  All nodes of graph are visited in BFS order
    :Time complexity: O(n2), where n is the number of next days to allocate meal prep for
    :Aux space complexity: O(n2), where n is the number of next days to allocate meal prep for
    """
    queue = [source]    # Queue to hold nodes yet to be visited
    visited_nodes = [False] * len(graph)  # Mark all nodes as unvisited in begining
    visited_nodes[source] = True   # Mark first node as visited

    while queue:  # Continue as long as we have nodes to visit
        node = queue.pop(0)   # Pop first node to visit
        for i in range(len(graph[node])):    # Vist all neighbours of visited node
            if visited_nodes[i] is False and graph[node][i] > 0:   # If node is still unvisited and has edge
                visited_nodes[i] = True  # Mark node as visited
                parent_graph[i] = node   # Mark node in parent graph
                queue.append(i)   # Append to yet to be visited queue
    return visited_nodes[sink]


def ford_fulkerson(graph: list, ff_source: int, ff_sink: int) -> int:
    """
    Sets initial flow to zero on all edges. While an augmenting path exists in the residual network,
    Augments the flow as much as possible along that path. Finally, flow should be max when no more
    flow can be pushed, and max flow is returned
    :Input:
        graph:  Network flow graph to search breadth-first
        ff_source:  Source node to start algorithm from
        ff_sink:   Sink node to end algorithm at
    :Output, return or postcondition: Maximum flow pushed along network
    :Time complexity: O(n2), where n is the number of next days to allocate meal prep for
    :Aux space complexity: O(n2), where n is the number of next days to allocate meal prep for
    """
    parent_graph = [-1] * (len(graph))   # parent graph
    max_flow = 0   # Set max flow to zero

    while bread_first_search(graph, ff_source, ff_sink, parent_graph):  # Until sink has been visited
        flowing_path = float("Inf")
        s = ff_sink   # Store sink

        while s != ff_source: # Until sink has been reached
            flowing_path = min(flowing_path, graph[parent_graph[s]][s])   # Chose smaller flow path
            s = parent_graph[s]   # Store sink

        end = ff_sink   # Store sink
        max_flow += flowing_path   # Increment max flow by flowing path

        while end != ff_source:   # Until end has been reached
            start = parent_graph[end]    # Update start
            graph[end][start] += flowing_path   # Update path flow
            graph[start][end] -= flowing_path   # Update path flow
            end = parent_graph[end]   # Update end
    return max_flow


class Node:

    def __init__(self) -> None:
        """
        Represents each node in the Suffix Tree. Uses an array to store child nodes at the index they represent
        :Input: None
        :Output, return or postcondition: New node with no children is created
        :Time complexity:O(1), where M and N denote the length of strings submission1 and submission2, respectively
        :Aux space complexity:O(1), where M and N denote the length of strings submission1 and submission2, respectively
        """
        self.children = [None] * 29


class SuffixTree:

    def __init__(self) -> None:
        """
        Represents all Suffixes of string in the form of a suffix tree.
        Starts off with one root node. Stores current greatest match
        :Input: None
        :Output, return or postcondition: Suffix Tree is initialized with root Node
        :Time complexity:O(1), where M and N denote the length of strings submission1 and submission2, respectively
        :Aux space complexity:O(1), where M and N denote the length of strings submission1 and submission2, respectively
        """
        self.root = Node()
        self.match = ""

    def insert(self, suffix: str) -> None:
        """
        Start at root of tree and insert each character into the Suffix tree. Create a new node at character index
        if it doesn't exist already. If exists append to sources to match similarity once inserted.
        :Input:
            suffix: Suffix of word we want to insert into the Suffix tree
        :Output, return or postcondition: Suffix is inserted in the Suffix tree, and match updated
        :Time complexity:O(N+M), where M and N denote the length of strings submission1 and submission2, respectively
        :Aux space complexity:O(N+M), where M and N denote the length of strings submission1 and submission2, respectively
        """
        word = self.root
        sources = []  # Store each character of a matched suffix

        for each_character in range(len(suffix)):  # Iterate over each character in suffix
            index = ord(suffix[each_character]) - ord('a')  # Get ascii code to insert node in array

            if word.children[index] is None:  # Create new node at index if character doesn't exist
                word.children[index] = Node()

            else:  # Add character to sources if it exists, so that similarity can be calculated
                sources.append(suffix[each_character])

            word = word.children[index]  # Move to current Node/word

        match = "".join(sources)  # Join matched word
        if len(match) > len(self.match):  # Update if it is the deepest internal node
            self.match = match


def build_suffix(submission1: str, submission2: str) -> SuffixTree:
    """
    Take both submissions and add string terminators at end, concatenate, and replace spaces with placeholder character.
    Create a new generalized Suffix Tree, insert each suffix
    :Input:
        submission1: First text submission to compare
        submission2: Second text submission to compare
    :Output, return or postcondition: Generalized Suffix tree is built with all suffixes of string
    :Time complexity: O((N+M)2), where M and N denote the length of strings submission1 and submission2, respectively
    :Aux space complexity: O((N+M)2), where M and N denote the length of strings submission1 and submission2, respectively
    """
    temp = [submission1, '{', submission2, '}']  # Add string terminators to ends of each submission
    total = "".join(temp)  # Join two strings so that generalized suffix tree can be constructed

    total = total.replace(' ', '|')  # Replace spaces with placeholder character
    suffix_tree = SuffixTree()  # Build generalized suffix tree

    for i in range(len(total)):  # Iterate over each suffix of combined submission
        suffix_tree.insert(total[i:])  # Insert each suffix into generalized suffix tree

    return suffix_tree


def compute(suffix_tree: SuffixTree) -> str:
    """
    Takes highest similarity match of the suffix tree, replaces the placeholder character back with spaces to get the
    longest common substring
    :Input:
        suffix_tree: Generalized Suffix tree built for strings
    :Output, return or postcondition: Longest Common Substring
    :Time complexity: O(N+M), where M and N denote the length of strings submission1 and submission2, respectively
    :Aux space complexity: O(N+M), where M and N denote the length of strings submission1 and submission2, respectively
    """
    similarity = suffix_tree.match  # Get greatest similarity
    similarity = similarity.replace('|', ' ')  # Replaces the placeholder character back
    return similarity


def compare_subs(submission1: str, submission2: str) -> list:
    """
    Return empty string if either submission is empty, return submission if it is a one letter char, and exists in
    the other submission. Otherwise, build suffix tree, and compute longest common substring. Calculate percentage
    of similarity in each submission
    :Input:
        submission1: First text submission to compare
        submission2: Second text submission to compare
    :Output, return or postcondition: List of Longest Common Substring and similarity in each
    :Time complexity:O((N+M)2), where M and N denote the length of strings submission1 and submission2, respectively
    :Aux space complexity:O((N+M)2), where M and N denote the length of strings submission1 and submission2, respectively
    """
    longest_common_substring = min(submission1, submission2)  # Define lcs as smaller submission
    if len(submission1) == 0 or len(submission2) == 0:  # Return empty string if either submission is an empty string
        return ['', 0, 0]

    elif len(submission1) == 1:  # If either submission is one character only
        for char in submission2:
            if char == submission1:  # and it exists in the other submission
                longest_common_substring = submission1

    elif len(submission2) == 1:  # If either submission is one character only
        for char in submission1:
            if char == submission2:  # and it exists in the other submission
                longest_common_substring = submission2

    else:  # Otherwise
        suffix_tree = build_suffix(submission1, submission2)  # Build Suffix Tree
        longest_common_substring = compute(suffix_tree)  # Compute Longest Common Substring

    one = round(100 * len(longest_common_substring) / len(submission1))  # Similarity of first in second
    two = round(100 * len(longest_common_substring) / len(submission2))  # Similarity of second in first

    return [longest_common_substring, one, two]
