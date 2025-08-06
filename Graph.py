def edge_generator(size):
    edges = {}
    cell = 0
    for i in range(size):
        for j in range(size):
            if i == 0 and j == 0: # condition A1
                edges[cell] = [1, size]
            elif i == 0 and j == size-1: # condition A2
                edges[cell] = [size-2, 2*size-1]
            elif i == size-1 and j == size-1: # condition A3
                edges[cell] = [(size*size)-size-1, (size**2)-2]
            elif i == size-1 and j == 0: # condition A4
                edges[cell] = [(i-1)*size,size*i+1]


            elif i == 0: # condition B1
                edges[cell] = [j-1, (i+1)*size+j,j+1]
            elif j == size-1: # condition B2
                edges[cell] = [i*size-1, ((i+1)*size)-2, (i+2)*size-1]
            elif i == size-1: # condition B3
                edges[cell] = [size*i+j-1, size*(i-1)+j,i*size+j+1]
            elif j == 0: # condition B4
                edges[cell] = [(i-1)*size, (i)*size+1, (i+1)*size]
            
            else:
                edges[cell] = [i*size+j+1, (i-1)*size+j, i*size+j-1, (i+1)*size+j] # condition C
            cell+=1
    return edges

# g = int(input("Enter grid size: "))
g = 5
grid = edge_generator(g)
print (grid)

# vis = [[]]
# for i in grid:
#     for j in range(len(grid[i])):
#         vis[i].append(grid[j])
import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(adj):
    # Example adjacency list

    # Create an undirected graph
    G = nx.Graph()

    # Add edges from adjacency list
    for node, neighbors in adj.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Draw the graph
    pos = nx.spring_layout(G)  # or use nx.kamada_kawai_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1000,
            edge_color='gray', font_weight='bold')

    plt.title("Graph from Adjacency List")
    plt.show()

# Call the function
draw_graph(grid)

