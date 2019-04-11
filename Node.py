class Node:

    def __init__(self, name):
        self.name = name
        self.neighbours = set()

    def add_neighbour(self, neighbour):
        self.neighbours.add(neighbour)

    def check_neighbour(self, neighbour):
        if neighbour in self.neighbours:
            return True
        return False

    def get_neighbours(self):
        return self.neighbours

    def get_name(self):
        return self.name