from __future__ import print_function

import networkx as nx
import random
import math
import pickle

# A -> B: A follow B
# successors(n): Return nodes followed by n.
# predecessors(n): Return node n's follower.


class Cascade:
    NOT_INFORMED = 0
    INFORMED = 1
    ADOPTED_WEEK = "AdoptedWeek"
    ADOPTED_NEIGHBORS = "AdoptedNeightbors"

    def __init__(self, g, p):
        self.network = g
        self.p = p
        # HashMap Node information
        # key: NodeId (int)
        # value:
        # "AdoptedWeek": int
        # "AdoptedNeightbors": [int list]
        self.neighbor_informations = {}
        for n in g.nodes():
            self.neighbor_informations[n] = {self.ADOPTED_WEEK: -1, self.ADOPTED_NEIGHBORS: [0]}

    @staticmethod
    def create_random_graph(population):
        """
        """
        g = nx.DiGraph()
        g.add_nodes_from(range(population))

        node_list = []
        for n in g.nodes():
            node_list.append(n)

        if len(node_list) != population:
            print("Node list number do not much!")

        # Generate Edges
        # Random out/in edges
        for v in g.nodes():
            num_out_edges = random.randint(0, population / 2)
            num_in_edges = random.randint(0, population / 2)

            out_targets = random.sample(node_list, num_out_edges)
            for t in out_targets:
                g.add_edge(v, t)

            in_targets = random.sample(node_list, num_in_edges)
            for s in in_targets:
                g.add_edge(s, v)

        print("Graph have", g.number_of_edges(), "edges.")
        g.remove_edges_from(g.selfloop_edges())
        print("After clean up graph have", g.number_of_edges(), "edges.")

        return g

    def generate_cascade_result(self, stop_weeks):
        # global neighbor_informations
        self.period0()
        weeks = 1

        keep_running = True
        while keep_running:
            self.period1(weeks)
            if weeks >= stop_weeks:
                keep_running = False
            weeks += 1
        print(self.neighbor_informations)

    def get_informed_num(self):
        """ Return number of informed nodes """
        informed_nodes = sum([1 for n in self.network.nodes(data=True) if n[1][self.INFORM_KEY] == self.INFORMED])
        return informed_nodes

    def period1(self, current_week):
        informed_nodes = set()
        for n in self.network.nodes():
            if self.neighbor_informations[n][self.ADOPTED_WEEK] != -1:
                continue  # Skip informed nodes
            else:
                m = 0.0

                neighbors = self.network.successors(n)

                for neighbor in neighbors:
                    if self.neighbor_informations[neighbor][self.ADOPTED_WEEK] != -1:
                        m += 1
                self.neighbor_informations[n][self.ADOPTED_NEIGHBORS].append(int(m))
                informed_threshold = 1 - pow(1 - self.p, m)
                u = random.uniform(0, 1)

                if u < informed_threshold:  # Adopted
                    informed_nodes.add(n)

        # Update informed nodes in period 2
        for n in informed_nodes:
            if self.neighbor_informations[n][self.ADOPTED_WEEK] != -1:
                print("ERROR! Node already informed!")
            self.neighbor_informations[n][self.ADOPTED_WEEK] = current_week

    def period0(self):
        """
            Select seed, select 10% celebrities as seed.
        """
        followers = {n: len(self.network.predecessors(n)) for n in self.network.nodes()}
        mean = float(sum(followers.values())) / len(followers)
        std_value = math.sqrt(sum([(n - mean) ** 2 for n in followers.values()]) / float(len(followers)))
        celebrity_threshold = mean + std_value  # Threshold is mean + 2 * standard deviation
        print("celebrity threshold(follower number) is {}".format(celebrity_threshold))
        celebrities = []
        for n in self.network.nodes():
            if len(self.network.predecessors(n)) >= celebrity_threshold:
                celebrities.append(n)
        print("Got {} celebrities, {:.2f}% of whole population.".format(len(celebrities),
                                                                        (float(len(celebrities)) / len(
                                                                            followers)) * 100))

        seeds_number = int(len(celebrities) / 10)
        print("Choose {} celebrities as seeds".format(seeds_number))
        for n in random.sample(celebrities, seeds_number):
            self.neighbor_informations[n][self.ADOPTED_WEEK] = 0

    def save(self, file):
        pickle.dump(self.neighbor_informations, file)