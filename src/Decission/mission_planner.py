from numpy import sign

offset_ascii = 65

class Node:
    """
    Node class for representing a point in the graph.
    """

    def __init__(self, x: int, y: int, name: str = '-'):
        """
        Initialize a Node.

        Args:
            x (int): X coordinate of the node.
            y (int): Y coordinate of the node.
            name (str): Name of the node.
        """
        self.x = x
        self.y = y
        self.name = name
        self.neighbours = []

    def add_neighbour(self, node: 'Node'):
        """
        Add a neighbour to the node.

        Args:
            node (Node): Neighbour node to be added.
        """
        self.neighbours.append(node)

    def remove_neighbour(self, node: 'Node'):
        """
        Remove a neighbour from the node.

        Args:
            node (Node): Neighbour node to be removed.
        """
        self.neighbours.remove(node)

    def get_neighbours(self) -> list:
        """
        Get the list of neighbour node names.

        Returns:
            list: List of neighbour node names.
        """
        return [node.name for node in self.neighbours]


class Graph:
    """
    Graph class for representing the environment as a grid of nodes.
    """

    def __init__(self, width: int, height: int, origin_name: str = None, dest_name: str = None):
        """
        Initialize a Graph.

        Args:
            width (int): Width of the graph.
            height (int): Height of the graph.
            origin_name (str, optional): Name of the origin node.
            dest_name (str, optional): Name of the destination node.
        """
        self.width = width
        self.height = height
        self.nodes = []
        self.create_graph()
        if origin_name is not None:
            self.origin = self.get_node_by_name(origin_name)
        if dest_name is not None:
            self.dest = self.get_node_by_name(dest_name)
        self.path = []
        self.directions = []
        self.current_pos = None
        self.going_to = None
        self.current_direction = [1, 0]
        self.test_8 = False

    def set_trajectory(self):
        """
        Set the trajectory from the origin to the destination.
        """
        if self.origin is None or self.dest is None:
            print("Please define origin and destination!")
            return 

        self.path = self.BFS(self.origin.name, self.dest.name)
        self.directions = self.get_directions(self.path)
        self.current_pos = self.origin
        self.going_to = self.path.pop(0)

    def update_trajectory(self, verbose: bool = False) -> tuple:
        """
        Update the trajectory to the next position and direction.

        Args:
            verbose (bool, optional): If True, prints current state information.

        Returns:
            tuple: New position and direction.
        """
        new_dir = self.directions.pop(0)
        new_pos = self.path.pop(0)

        if verbose:
            print("You are currently at:", self.current_pos.name)
            print("You currently have the following direction:", self.current_direction)
            print("You need to go to:", self.going_to.name)

        return new_pos, new_dir

    def get_next_action(self) -> int:
        """
        Get the next action based on the current trajectory.

        Returns:
            int: The next action.
        """
        if self.test_8:
            return 5

        if len(self.path) == 0:
            # Stop, found target
            return 1

        new_loc, new_dir = self.update_trajectory()

        x_new, y_new = new_dir
        x_old, y_old = self.current_direction
        self.current_direction = new_dir
        self.current_pos = self.going_to
        self.going_to = new_loc

        if x_old == x_new and y_old == y_new:
            # Go straight
            return 5

        if x_new + x_old == 0 and y_new == y_old:
            # Turn 180
            return 4
        if y_new + y_old == 0 and x_old == x_new:
            # Turn 180
            return 4

        if y_new == 0:
            if sign(y_old) == sign(x_new):
                # Turn left
                return 3
            else:
                # Turn right
                return 2

        if x_new == 0:
            if sign(x_old) == sign(y_new):
                # Turn right
                return 2
            else:
                # Turn left
                return 3

    def translate_actions(self, action: int):
        """
        Translate the action to a human-readable format and print it.

        Args:
            action (int): The action to be translated.
        """
        actions = {
            1: "Stop",
            2: "Turn right",
            3: "Turn left",
            4: "Turn 180 degrees",
            5: "Pass"
        }
        print(actions.get(action, str(action)))

    def simulate_path(self):
        """
        Simulate the path by executing actions until the destination is reached.
        """
        action = self.get_next_action()
        count = 0
        while action != 1:
            print("---------")
            print("Current pos:", self.current_pos.name)
            print("Going to:", self.going_to.name)
            print("Current dir:", self.current_direction)
            self.translate_actions(action)
            if count == 2:
                action = self.obstacle_found()
            else:
                action = self.get_next_action()
            count += 1

    def obstacle_found(self) -> int:
        """
        Handle the event when an obstacle is found.

        Returns:
            int: Action to turn 180 degrees.
        """
        self.origin = self.current_pos
        self.remove_edge(self.current_pos.name, self.going_to.name)
        self.print_graph()
        self.path = self.BFS(self.origin.name, self.dest.name)
        self.directions = self.get_directions(self.path)
        self.current_direction = [-self.current_direction[0], -self.current_direction[1]]
        self.going_to = self.path.pop(0)
        return 4

    def create_graph(self):
        """
        Create the graph with nodes and their neighbours.
        """
        for i in range(self.height):
            for j in range(self.width):
                self.nodes.append(Node(j, i, chr(offset_ascii + i * self.width + j)))

        for node in self.nodes:
            if node.x != 0:
                node.add_neighbour(self.nodes[node.y * self.width + node.x - 1])
            if node.x != self.width - 1:
                node.add_neighbour(self.nodes[node.y * self.width + node.x + 1])
            if node.y != 0:
                node.add_neighbour(self.nodes[(node.y - 1) * self.width + node.x])
            if node.y != self.height - 1:
                node.add_neighbour(self.nodes[(node.y + 1) * self.width + node.x])

    def print_graph(self):
        """
        Print the graph in a readable format.
        """
        for i in range(self.height):
            for j in range(self.width):
                if j != 0:
                    if self.nodes[i * self.width + j - 1] in self.nodes[i * self.width + j].neighbours:
                        print(" - ", end="")
                    else:
                        print("   ", end="")
                current_node = self.nodes[i * self.width + j]
                print(current_node.name, end="")
            print("")

            if i == self.width - 1:
                continue
            for j in range(self.width):
                if self.nodes[(i + 1) * self.width + j] in self.nodes[i * self.width + j].neighbours:
                    print("|   ", end="")
                else:
                    print("    ", end="")
            print("")

    def get_node(self, x: int, y: int) -> Node:
        """
        Get a node by its coordinates.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.

        Returns:
            Node: The node at the given coordinates.
        """
        return self.nodes[y * self.height + x]

    def get_node_by_name(self, name: str) -> Node:
        """
        Get a node by its name.

        Args:
            name (str): Name of the node.

        Returns:
            Node: The node with the given name.
        """
        pos = ord(name) - offset_ascii
        return self.nodes[pos]

    def remove_edge(self, node1_name: str, node2_name: str):
        """
        Remove the edge between two nodes.

        Args:
            node1_name (str): Name of the first node.
            node2_name (str): Name of the second node.
        """
        node1 = self.get_node_by_name(node1_name)
        node2 = self.get_node_by_name(node2_name)
        node1.neighbours.remove(node2)
        node2.neighbours.remove(node1)

    def dummy_path(self, origin_name: str, dest_name: str) -> list:
        """
        Generate a dummy path from the origin to the destination.

        Args:
            origin_name (str): Name of the origin node.
            dest_name (str): Name of the destination node.

        Returns:
            list: List of node names in the path.
        """
        origin = self.get_node_by_name(origin_name)
        dest = self.get_node_by_name(dest_name)
        delta_x = dest.x - origin.x
        delta_y = dest.y - origin.y
        path = []

        for i in range(1, delta_x + 1):
            next_x = origin.x + i * sign(delta_x)
            path.append(self.get_node(next_x, origin.y))

        for i in range(1, delta_y + 1):
            next_y = origin.y + i * sign(delta_y)
            path.append(self.get_node(origin.x + delta_x, next_y))

        return [node.name for node in path]

    def BFS(self, origin_name: str, dest_name: str, names_only: bool = False) -> list:
        """
        Perform a Breadth-First Search (BFS) from the origin to the destination.

        Args:
            origin_name (str): Name of the origin node.
            dest_name (str): Name of the destination node.
            names_only (bool, optional): If True, returns node names only.

        Returns:
            list: Path from origin to destination.
        """
        origin = self.get_node_by_name(origin_name)
        dest = self.get_node_by_name(dest_name)
        visited = set()
        to_visit = []
        parent = {}
        current_node = origin
        end = False

        while len(visited) < len(self.nodes):
            if current_node == dest:
                end = True
                break
            visited.add(current_node)
            for neighbour in current_node.neighbours:
                if neighbour not in visited:
                    parent[neighbour] = current_node
                    to_visit.append(neighbour)
            current_node = to_visit.pop(0)

        if not end:
            print("No path available!")
        else:
            path = []
            while current_node != origin:
                path.append(current_node)
                current_node = parent[current_node]
            path.append(origin)
            path.reverse()

            if names_only:
                path = [node.name for node in path]

            return path

    def get_directions(self, path: list) -> list:
        """
        Get the directions for the given path.

        Args:
            path (list): List of nodes in the path.

        Returns:
            list: List of directions for the path.
        """
        directions = []
        path_copy = path.copy()
        while True:
            current_node = path_copy.pop(0)
            direction = [0, 0]
            if len(path_copy) == 0:
                return directions

            if path_copy[0].x < current_node.x:
                direction[0] = -1
            elif path_copy[0].x > current_node.x:
                direction[0] = 1

            if path_copy[0].y < current_node.y:
                direction[1] = -1
            elif path_copy[0].y > current_node.y:
                direction[1] = 1

            directions.append(direction)


if __name__ == "__main__":
    graph = Graph(5, 5, "A", "S")
    graph.print_graph()
    graph.set_trajectory()
    graph.simulate_path()
    final_dir = graph.current_direction
    graph = Graph(5, 5, "S", "A")
    graph.current_direction = final_dir
    graph.set_trajectory()
    graph.simulate_path()





    
