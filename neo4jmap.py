import pandas as pd
from Node import Node
import time
from neo4jrestclient.client import GraphDatabase
db = GraphDatabase("http://localhost:7474", username="neo4j",
                       password="n3o4j")


def relation():
    df = pd.read_csv("filemapc.csv")
    relation = {}
    node_idmap = {}
    db = GraphDatabase("http://localhost:7474", username="neo4j",
                       password="n3o4j")
    committer_email = db.labels.create("CommitterEmail")

    # bob in [rel.end for rel in alice.relationships.all(types=['Knows'])]

    for idx, x in df['committers'].iteritems():
        commiters = x.split()
        first_committer = commiters.pop(0)
        print()
        print("file", idx)
        print("first committer is", first_committer)
        if first_committer not in relation:
            x = Node(first_committer)
            relation[first_committer] = x
            n_new = db.nodes.create(name=first_committer)
            n_nid = n_new.id
            # print(n_nid)
            committer_email.add(n_new)
            node_idmap[first_committer] = n_nid
            # print(node_idmap)
            print("commiter created:", relation[first_committer].get_name())

        if len(commiters) !=0:
            for commiter in commiters:
                # if the committer object exists, check if they are already
                # neighbours
                # if not, add them as neighbours
                # if already exist then ignore
                if commiter in relation:
                    if not relation[commiter].check_neighbour(first_committer):
                        prev = relation[commiter]
                        prev.add_neighbour(first_committer)

                        # print(prev.get_neighbours())
                        relation[commiter] = prev
                        n1 = db.nodes.get(node_idmap[commiter])
                        n2 = db.nodes.get(node_idmap[first_committer])
                        n1.Knows(n2)

                        prev = relation[first_committer]
                        prev.add_neighbour(commiter)
                        relation[first_committer] = prev

                        print(commiter, 'added this person as neighbor ->', first_committer)
                # if committer node does not exist, create it and add them as
                # neighbors
                else:
                    x = Node(commiter)
                    relation[commiter] = x
                    n_new = db.nodes.create(name=commiter)
                    n_nid = n_new.id
                    # print(n_nid)
                    node_idmap[commiter] = n_nid
                    # print(node_idmap)
                    committer_email.add(n_new)

                    prev = relation[first_committer]
                    prev.add_neighbour(commiter)
                    print(prev.get_neighbours())
                    relation[first_committer] = prev

                    # print(node_idmap[first_committer])
                    n1 = db.nodes.get(node_idmap[commiter])
                    n2 = db.nodes.get(node_idmap[first_committer])
                    n2.Knows(n1)
                    print(first_committer, 'added this person as neighbor ->',
                          commiter)
        else:
            print("just one commiter in file")
            print()


def main():
    start_time = time.time()
    relation()
    print("--- %s seconds to node the file ---" % (time.time() -
                                                  start_time))


if __name__ == '__main__':
    main()