# Topogen

A simple tool to generate network topologies based on an abstract graph representation.

## Features

- **Graph-Based Generation**: Create complex network topologies from a simple 2D matrix.
- **Node Placement**: Automatically assigns grid coordinates to each node.
- **Relationship Mapping**: Establishes parent, child, and conflict relationships between nodes.
- **Dynamic Link Characteristics**: Calculates link data rates based on physical models (e.g., Shannon Capacity) and the distance between nodes.
- **Pathfinding**: Finds all possible paths from the donor (root) node to all other nodes in the network.
- **Supported Topologies**: Generates Directed Acyclic Graph (DAG) or Tree structures.
- **Simulation Helper**: Includes a basic `info_exchange` function to simulate one-hop message passing.

## Installation

Clone the repository and install the package using pip.

```bash
git clone https://github.com/lucasjinhong/topogen.git
cd topogen
pip install .
```

## Usage

Here is a basic example of how to generate a network topology.

1.  **Define a graph matrix**: Create a 2D list where `1` represents a potential node location. The generator will place a donor node at the first `1` in the first row and build the network from there.
2.  **Generate the topology**: Call `generate_topology_from_graph` with your matrix and desired parameters.
3.  **Explore the result**: The returned `Topo` object contains all the information about your network, including nodes, links, and paths.

```python
from topogen import generate_topology_from_graph

# 1. Define the topology structure as a matrix.
# '1' represents a potential node location.
graph_matrix = [
    [0, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 1, 0, 1]
]

# 2. Generate the topology.
# Parameters: graph, tree_type, max_connection_distance, grid_unit_length_in_meters
try:
    topo = generate_topology_from_graph(
        graph=graph_matrix,
        tree_type='DAG',
        max_dist_to_connect_nodes=1.5,
        size_of_grid_len=10
    )

    # 3. Access the generated topology data.
    print(f"Generated {len(topo.nodes)} nodes and {len(topo.links)} links.")

    # Print the name of each node and its properties
    print("\n--- Nodes ---")
    for node_name, node in topo.nodes.items():
        print(f"Node '{node_name}': Type={node.type}, Coords={node.coordinate}")

    # Print the links and their calculated data rates
    print("\n--- Links ---")
    for link_name, link in topo.links.items():
        print(f"Link {link.name}: {link.src_node.name} -> {link.dst_node.name}, Data Rate: {link.data_rate_bps:.2f} bps")

    # Print the final graph representation with node names
    print("\n--- Final Graph Representation ---")
    for row_index, row in topo.topo_graph.items():
        print(row)

except ValueError as e:
    print(f"Error generating topology: {e}")

```

## Testing

This project uses `pytest` for testing. To run the tests, install the testing dependencies and run `pytest` from the project root.

```bash
# Install testing requirements
pip install pytest pytest-cov

# Run tests
pytest
```

## License

This project is licensed under the MIT License.
