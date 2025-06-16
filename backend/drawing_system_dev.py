import squarify
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import math
import copy
import heapq
import os
import re
import random
import difflib
import cv2
from shapely.geometry import Polygon, LineString, Point

# Function to find the most similar room name if not directly available
def find_closest_room(room_name, valid_room_names):
    closest_match = difflib.get_close_matches(room_name, valid_room_names, n=1, cutoff=0.6)
    return closest_match[0] if closest_match else "storeroom"  # Default to 'storeroom' if no close match

# Generate constraints while preserving mappings with underscores
def get_constraints_room_mappings(user_constraints, room_sizes):
    constraints = []
    room_name_mappings = {}
    valid_room_names = list(room_sizes.keys())

    for room in user_constraints['indoor_room_info']:
        original_room_name = room["name"]  # e.g., 'bedroom1' or 'bedroom_1'
        cleaned_room_name = original_room_name.replace("_", "").lower()  # e.g., 'bedroom1'
        room_size = room["size"].lower()

        # Determine the closest valid room type
        if cleaned_room_name in room_sizes:
            mapped_room = original_room_name  # Already valid
        else:
            closest_match = find_closest_room(cleaned_room_name, valid_room_names)

            # Extract numeric suffix (if any)
            suffix_match = re.search(r'\d+$', original_room_name)
            suffix = f"_{suffix_match.group()}" if suffix_match else ""

            mapped_room = closest_match + suffix

        # Preserve the mapping of original name to mapped room name
        room_name_mappings[original_room_name] = mapped_room

        # Assign size value using room_sizes, fallback to 5 if not found
        base_room_type = mapped_room.split("_")[0]
        size_value = room_sizes.get(base_room_type, {}).get(room_size, 5)

        constraints.append({"type": mapped_room, "size": size_value})

    # Output result
    print("Constraints:", constraints)
    print("Room Name Mappings:", room_name_mappings)
    return constraints, room_name_mappings

def group_rooms(constraints, area_types):
    grouped_rooms = {"social": [], "service": [], "private": []}
    livingroom = None

    for room in constraints:
        room_name = room["type"]
        base_name = room_name.split("_")[0]
        area_type = area_types.get(base_name, None)

        if base_name == "livingroom":
            livingroom = {"name": room_name, "size": room["size"]}

        elif area_type:
            grouped_rooms[area_type].append({"name": room_name, "size": room["size"]})

    # Ensure livingroom_1 exists and is first in the social area
    if not livingroom:
        livingroom = {"name": "livingroom_1", "size": 12}
    
    grouped_rooms["social"].insert(0, livingroom)

    # Remove groups that are empty (except social)
    for area in ["private", "service"]:
        if not grouped_rooms[area]:
            del grouped_rooms[area]

    return grouped_rooms


def squarify_areas(grouped_rooms):
    area_sizes = {area: sum(r["size"] for r in rooms) for area, rooms in grouped_rooms.items()}
    norm_area_sizes = squarify.normalize_sizes(list(area_sizes.values()), 100, 100)
    areas = squarify.squarify(norm_area_sizes, x=0, y=0, dx=100, dy=100)
    return areas


def allocate_rooms(rooms, area):
    room_sizes = [r["size"] for r in rooms]
    room_labels = [r["name"] for r in rooms]
    norm_sizes = squarify.normalize_sizes(room_sizes, area["dx"], area["dy"])
    return squarify.squarify(norm_sizes, x=area["x"], y=area["y"], dx=area["dx"], dy=area["dy"]), room_labels


# Function to check if two rooms share an edge
def share_edge(rect1, rect2, door_length=2, tol=1e-5):
    x1, y1, w1, h1 = rect1["x"], rect1["y"], rect1["dx"], rect1["dy"]
    x2, y2, w2, h2 = rect2["x"], rect2["y"], rect2["dx"], rect2["dy"]

    # Check vertical adjacency
    vertical_overlap = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
    vertical_touch = (abs(x1 - (x2 + w2)) < tol or abs(x2 - (x1 + w1)) < tol) and vertical_overlap >= door_length

    # Check horizontal adjacency
    horizontal_overlap = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
    horizontal_touch = (abs(y1 - (y2 + h2)) < tol or abs(y2 - (y1 + h1)) < tol) and horizontal_overlap >= door_length

    return vertical_touch or horizontal_touch

def build_graph(room_data):
    # Create an undirected graph
    graph = nx.Graph()

    # Add nodes with labels
    for i, data in room_data.items():
        graph.add_node(i, label=data["label"])

    # Add edges based on shared edges
    for i, data1 in room_data.items():
        for j, data2 in room_data.items():
            if i < j and share_edge(data1["rect"], data2["rect"]):  
                graph.add_edge(i, j)

    return graph

def get_room_data_and_graph(grouped_rooms, squarified_areas):
    room_data = {}  # Dictionary to store room data
    room_id = 0  # Unique identifier for each room

    for (area, area_rect) in zip(grouped_rooms.keys(), squarified_areas):
        rects, labels = allocate_rooms(grouped_rooms[area], area_rect)
        
        # Store each room's data in the dictionary
        for rect, label in zip(rects, labels):
            room_data[room_id] = {"label": label, "rect": rect}
            room_id += 1
    # Add adjacency information to room_data
    for i in room_data:
        room_data[i]["adjacent_rooms"] = [
            j for j in room_data if i != j and share_edge(room_data[i]["rect"], room_data[j]["rect"])
        ]
    graph = build_graph(room_data)

    return room_data, graph


def plot_treemap(room_data):
    # Plot the treemap using room_data
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_facecolor("gray")

    for i, data in room_data.items():
        rect = data["rect"]
        x, y, w, h = rect["x"], rect["y"], rect["dx"], rect["dy"]
        ax.add_patch(plt.Rectangle((x, y), w, h, facecolor="gray", edgecolor="black", linewidth=5))
        ax.text(x + w / 2, y + h / 2, data["label"], ha="center", va="center", fontsize=10, color="black")

    plt.show()
    plt.show()  # Show plot without blocking execution
    plt.close()  # Immediately close the plot window

def plot_graph(graph, room_data):
    # Plot the adjacency graph
    plt.figure(figsize=(8, 8))
    pos = {i: (room_data[i]["rect"]["x"] + room_data[i]["rect"]["dx"] / 2, 
            room_data[i]["rect"]["y"] + room_data[i]["rect"]["dy"] / 2) 
        for i in graph.nodes}

    nx.draw(graph, pos, labels={i: room_data[i]["label"] for i in graph.nodes}, with_labels=True, node_size=3000, node_color="lightblue")
    plt.show()  # Show plot without blocking execution
    plt.close()  # Immediately close the plot window

def normalize_label(label):
    """Removes numerical suffix from room labels for comparison."""
    return label.split("_")[0]

def get_swappable_rooms(room_data):
    """Finds pairs of adjacent rooms that can be swapped based on alignment."""
    TOLERANCE = 1e-3  
    swappable_rooms = []

    for i, room1 in room_data.items():
        for j in room1['adjacent_rooms']:
            if i >= j:  # Avoid duplicate pairs
                continue

            room2 = room_data[j]

            # Compare room types without numerical suffixes
            if normalize_label(room1['label']) == normalize_label(room2['label']):
                rect1, rect2 = room1['rect'], room2['rect']

                # Check if they align along x-axis or y-axis
                same_x = math.isclose(rect1['x'], rect2['x'], abs_tol=TOLERANCE) and \
                         math.isclose(rect1['dx'], rect2['dx'], abs_tol=TOLERANCE)
                same_y = math.isclose(rect1['y'], rect2['y'], abs_tol=TOLERANCE) and \
                         math.isclose(rect1['dy'], rect2['dy'], abs_tol=TOLERANCE)

                if same_x or same_y:
                    swappable_rooms.append((i, j))

    return swappable_rooms

def swap_rooms(room_data, pair):
    """Swaps positions of two rooms (visually) and updates adjacency references accordingly."""
    i, j = pair
    TOLERANCE = 1e-3  
    swapped_room_data = copy.deepcopy(room_data)

    # Swap positions (rects) only
    rect1, rect2 = swapped_room_data[i]["rect"], swapped_room_data[j]["rect"]

    if math.isclose(rect1['x'], rect2['x'], abs_tol=TOLERANCE) and math.isclose(rect1['dx'], rect2['dx'], abs_tol=TOLERANCE):
        rect1["y"], rect2["y"] = rect2["y"], rect1["y"]
    elif math.isclose(rect1['y'], rect2['y'], abs_tol=TOLERANCE) and math.isclose(rect1['dy'], rect2['dy'], abs_tol=TOLERANCE):
        rect1["x"], rect2["x"] = rect2["x"], rect1["x"]

    # 🔄 Now update all adjacent_rooms to reflect the swapped indices
    for k, room in swapped_room_data.items():
        updated_adj = []
        for adj in room['adjacent_rooms']:
            if adj == i:
                updated_adj.append(j)
            elif adj == j:
                updated_adj.append(i)
            else:
                updated_adj.append(adj)
        room['adjacent_rooms'] = updated_adj

    return swapped_room_data


def plot_graph_and_contour(graph_data, path, padding=5):
    vertices = graph_data["vertices"]
    edges = graph_data["edges"]

    # Determine min and max coordinates
    all_x = [v[0] for v in vertices]
    all_y = [v[1] for v in vertices]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Apply padding
    min_x -= padding
    max_x += padding
    min_y -= padding
    max_y += padding

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_facecolor("white")

    # Plot original graph (black edges)
    for (v1, v2) in edges:
        x_values = [v1[0], v2[0]]
        y_values = [v1[1], v2[1]]
        ax.plot(x_values, y_values, "k-", linewidth=5)  # Light black edges

    # Plot vertices (red dots)
    for vertex in vertices:
        ax.plot(vertex[0], vertex[1], "ro", markersize=4)

    for (v1, v2) in path:
        x_values = [v1[0], v2[0]]
        y_values = [v1[1], v2[1]]
        ax.plot(x_values, y_values, "g-", linewidth=5)
    plt.show()  # Show plot without blocking execution
    plt.close()  # Immediately close the plot window



def euclidean_distance(v1, v2):
    return math.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)

def shortest_path_to_connect_rooms(graph_data, entry_point, disconnected_rooms):
    vertices = graph_data['vertices']
    edges = graph_data['edges']

    # Priority queue for BFS-like search: (cost, current_vertex, path_edges, covered_rooms)
    pq = [(0, entry_point, [], set())]  
    visited = {}

    while pq:
        cost, current_vertex, path_edges, covered_rooms = heapq.heappop(pq)

        # If all disconnected rooms are covered, return the path
        if covered_rooms >= set(disconnected_rooms):
            return path_edges

        # If we reach a vertex with a better room coverage, update visited
        state = (current_vertex, frozenset(covered_rooms))
        if state in visited and visited[state] <= cost:
            continue
        visited[state] = cost

        # Explore neighbors
        for (v1, v2), edge_rooms in edges.items():
            if v1 == current_vertex or v2 == current_vertex:
                next_vertex = v2 if v1 == current_vertex else v1
                # new_cost = cost + 1  # Uniform edge weight
                new_cost = cost + euclidean_distance(current_vertex, next_vertex)
                new_path_edges = path_edges + [((v1, v2), edge_rooms)]
                
                # Track covered rooms
                new_covered_rooms = covered_rooms | set(edge_rooms)

                heapq.heappush(pq, (new_cost, next_vertex, new_path_edges, new_covered_rooms))

    return None  # No path found

def remove_outside_edges_and_corners(graph_data, grid_size=100):
    edges = graph_data["edges"].copy()  # Copy to avoid modifying original data
    vertices = graph_data["vertices"].copy()  # Copy to avoid modifying original data

    # Identify boundary edges
    boundary_edges = set()
    for (v1, v2) in graph_data["edges"].keys():
        if (0 in v1 or grid_size in v1) and (0 in v2 or grid_size in v2):
            boundary_edges.add((v1, v2))

    # Remove the boundary edges from the global edges dictionary
    for edge in boundary_edges:
        if edge in edges:
            del edges[edge]

    # Define corner vertices
    corner_vertices = {(0, 0), (grid_size, 0), (0, grid_size), (grid_size, grid_size)}

    # Remove corner vertices if they are present
    for corner in corner_vertices:
        if corner in vertices:
            del vertices[corner]

    return {
        "vertices": vertices,
        "edges": edges,
        "room_vertices": graph_data["room_vertices"],  # Keeping original room vertices
    }

def plot_treemap_absolute(room_data):
    # Plot the treemap using updated absolute coordinates
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_facecolor("gray")

    for i, data in room_data.items():
        rect = data["rect"]
        x1, y1, x2, y2 = rect["x1"], rect["y1"], rect["x2"], rect["y2"]
        width = x2 - x1
        height = y2 - y1

        ax.add_patch(plt.Rectangle((x1, y1), width, height, facecolor="gray", edgecolor="black", linewidth=4))
        ax.text(x1 + width / 2, y1 + height / 2, data["label"], ha="center", va="center", fontsize=10, color="black")

    plt.show()

def convert_to_absolute(room_data):
    new_room_data = {}
    for room_id, room in room_data.items():
        x = room['rect']['x']
        y = room['rect']['y']
        dx = x + room['rect']['dx']  # Convert width to absolute x2
        dy = y + room['rect']['dy']  # Convert height to absolute y2
        
        new_room_data[room_id] = {
            'label': room['label'],
            'rect': {'x1': x, 'y1': y, 'x2': dx, 'y2': dy},
            'adjacent_rooms': room['adjacent_rooms']
        }
    
    return new_room_data

def convert_to_graph_with_room_info(room_data):
    def round_vertex(v, precision=6):
        """Round a vertex to avoid floating-point precision errors."""
        return (round(v[0], precision), round(v[1], precision))

    vertices = {}  # {(x, y): [room_labels]}
    edges = {}  # {(v1, v2): [room_labels]}
    room_vertices = {}  # {room_label: [(x, y)]}

    # Step 1: Collect all room vertices first
    for room_id, room in room_data.items():
        room_label = room["label"]
        rect = room["rect"]
        x1, y1, x2, y2 = rect["x1"], rect["y1"], rect["x2"], rect["y2"]

        # Define four corners with rounding
        top_left = round_vertex((x1, y1))
        top_right = round_vertex((x2, y1))
        bottom_left = round_vertex((x1, y2))
        bottom_right = round_vertex((x2, y2))

        # Store room vertices
        room_vertices[room_label] = [top_left, top_right, bottom_left, bottom_right]

        # Add vertices to global dictionary
        for vertex in [top_left, top_right, bottom_left, bottom_right]:
            if vertex not in vertices:
                vertices[vertex] = []
            if room_label not in vertices[vertex]:  # Avoid duplicate labels
                vertices[vertex].append(room_label)

    # Step 2: Add edges with segmentation logic
    def get_intermediate_vertices(v1, v2):
        """Find all vertices that lie on the line segment between v1 and v2."""
        x1, y1 = v1
        x2, y2 = v2
        intermediate = []

        for v in vertices.keys():
            if v == v1 or v == v2:
                continue
            x, y = v

            # Check if the vertex is collinear and lies within the segment bounds
            if (x1 == x2 and x1 == x and min(y1, y2) < y < max(y1, y2)) or \
               (y1 == y2 and y1 == y and min(x1, x2) < x < max(x1, x2)):
                intermediate.append(v)

        return sorted(intermediate, key=lambda p: (p[0], p[1]))  # Sort for correct traversal

    for room_label, room_verts in room_vertices.items():
        edges_to_add = [
            (room_verts[0], room_verts[1]),  # Top edge
            (room_verts[1], room_verts[3]),  # Right edge
            (room_verts[2], room_verts[3]),  # Bottom edge
            (room_verts[0], room_verts[2]),  # Left edge
        ]

        for v1, v2 in edges_to_add:
            v1 = round_vertex(v1)
            v2 = round_vertex(v2)

            if v1 == v2:  # Prevent self-loops
                continue

            # Get any intermediate vertices between v1 and v2
            intermediate = get_intermediate_vertices(v1, v2)

            # If there are intermediate vertices, split the edge
            if intermediate:
                current = v1
                for mid in intermediate:
                    mid = round_vertex(mid)
                    edge = tuple(sorted((current, mid)))
                    if edge not in edges:
                        edges[edge] = []
                    edges[edge].append(room_label)
                    current = mid  

                edge = tuple(sorted((current, v2)))
                if edge not in edges:
                    edges[edge] = []
                edges[edge].append(room_label)
            else:
                edge = tuple(sorted((v1, v2)))
                if edge not in edges:
                    edges[edge] = []
                edges[edge].append(room_label)

    return {
        "vertices": vertices,
        "edges": edges,
        "room_vertices": room_vertices,
    }

def plot_graph_new(graph_data, padding=5):
    vertices = graph_data["vertices"]
    edges = graph_data["edges"]

    # Determine min and max coordinates
    all_x = [v[0] for v in vertices]
    all_y = [v[1] for v in vertices]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Apply padding
    min_x -= padding
    max_x += padding
    min_y -= padding
    max_y += padding

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_facecolor("white")

    # Plot edges
    for (v1, v2) in edges:
        x_values = [v1[0], v2[0]]
        y_values = [v1[1], v2[1]]
        ax.plot(x_values, y_values, "k-", linewidth=1)  # Black edges

    # Plot vertices
    for vertex in vertices:
        ax.plot(vertex[0], vertex[1], "ro", markersize=4)  # Red dots for vertices

    plt.show()  # Show plot without blocking execution
    plt.close()  # Immediately close the plot window

def plot_graph_edges(edges_dict, padding=5):
    """Plots edges from an edge dictionary using Matplotlib."""
    
    # Extract unique vertices from edges
    vertices = set()
    for edge in edges_dict.keys():
        vertices.update(edge)

    # Determine min and max coordinates
    all_x = [v[0] for v in vertices]
    all_y = [v[1] for v in vertices]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Apply padding
    min_x -= padding
    max_x += padding
    min_y -= padding
    max_y += padding

    # Create plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_facecolor("white")

    # Plot edges
    for (v1, v2) in edges_dict.keys():
        x_values = [v1[0], v2[0]]
        y_values = [v1[1], v2[1]]
        ax.plot(x_values, y_values, "k-", linewidth=4)  # Black edges
    plt.show()  # Show plot without blocking execution
    plt.close()  # Immediately close the plot window


# attach bathroom function

def add_attached_bathroom_to_room(
    room_name,
    room_edges_dict,
    edge_to_rooms,
    label_positions,
    width_fraction=0.5,
    depth_fraction=0.3,
    color='gray'
):
    # Get all edges that belong to the room
    relevant_edges = [edge for edge, rooms in edge_to_rooms.items() if room_name in rooms]

    if not relevant_edges:
        print(f"No edges found for room: {room_name}")
        return {}, {}

    # Select the longest edge
    def edge_length(edge):
        (x1, y1), (x2, y2) = edge
        return math.hypot(x2 - x1, y2 - y1)

    longest_edge = max(relevant_edges, key=edge_length)
    (x1, y1), (x2, y2) = longest_edge
    length = edge_length(longest_edge)

    # Midpoint of the edge
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2

    # Direction vectors
    dx, dy = x2 - x1, y2 - y1
    ux, uy = dx / length, dy / length  # unit tangent
    nx, ny = -uy, ux  # inward normal (choose later)

    # Determine inward normal (towards room center)
    room_center = label_positions[room_name]
    m1 = (mx + nx, my + ny)
    m2 = (mx - nx, my - ny)
    d1 = math.hypot(m1[0] - room_center[0], m1[1] - room_center[1])
    d2 = math.hypot(m2[0] - room_center[0], m2[1] - room_center[1])
    if d1 > d2:
        nx, ny = -nx, -ny

    # Width and depth
    attach_width = length * width_fraction
    attach_depth = length * depth_fraction

    # Compute bathroom polygon
    midx, midy = mx, my
    wx, wy = ux * attach_width / 2, uy * attach_width / 2
    dx, dy = nx * attach_depth, ny * attach_depth

    v1 = (midx - wx, midy - wy)
    v2 = (midx + wx, midy + wy)
    v3 = (v2[0] + dx, v2[1] + dy)
    v4 = (v1[0] + dx, v1[1] + dy)

    bathroom_poly = [v1, v2, v3, v4]

    return {room_name: bathroom_poly}


# helper functions

def create_side_segment(edge, fraction, from_start=True):
    """Returns a smaller segment starting from one end of the edge."""
    (x1, y1), (x2, y2) = edge
    dx, dy = x2 - x1, y2 - y1
    length = ((dx)**2 + (dy)**2) ** 0.5
    scale = fraction * length

    # Unit vector
    ux, uy = dx / length, dy / length

    if from_start:
        sx1, sy1 = x1, y1
        sx2, sy2 = x1 + ux * scale, y1 + uy * scale
    else:
        sx2, sy2 = x2, y2
        sx1, sy1 = x2 - ux * scale, y2 - uy * scale

    return (sx1, sy1), (sx2, sy2)

def create_centered_segment(edge, fraction):
    """Returns a smaller centered segment of the given edge."""
    (x1, y1), (x2, y2) = edge
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2  # center
    dx, dy = x2 - x1, y2 - y1
    length = ((dx)**2 + (dy)**2) ** 0.5
    scale = fraction * length / 2

    # Unit vector
    ux, uy = dx / length, dy / length
    sx1 = cx - ux * scale
    sy1 = cy - uy * scale
    sx2 = cx + ux * scale
    sy2 = cy + uy * scale

    return (sx1, sy1), (sx2, sy2)



def get_outside_edges_of_room(edges_dict, room_name):
    return [edge for edge, rooms in edges_dict.items() if len(rooms) == 1 and rooms[0] == room_name]

def pick_best_outside_edge(outside_edges):
    def edge_length(e):
        (x1, y1), (x2, y2) = e
        return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
    return max(outside_edges, key=edge_length) if outside_edges else None

def create_balcony_from_edge(edge, depth=5.0, room_center=None):
    (x1, y1), (x2, y2) = edge
    dx, dy = x2 - x1, y2 - y1
    length = (dx**2 + dy**2) ** 0.5
    if length == 0:
        return []

    # Unit vectors
    ux, uy = dx / length, dy / length
    nx1, ny1 = -uy, ux
    nx2, ny2 = uy, -ux

    def mid_point(edge):
        return ((edge[0][0] + edge[1][0]) / 2, (edge[0][1] + edge[1][1]) / 2)

    def offset_midpoint(nx, ny):
        mx, my = mid_point(edge)
        return (mx + nx * 0.5, my + ny * 0.5)

    # Choose outward normal
    m1 = offset_midpoint(nx1, ny1)
    m2 = offset_midpoint(nx2, ny2)
    dist1 = ((m1[0] - room_center[0]) ** 2 + (m1[1] - room_center[1]) ** 2) ** 0.5
    dist2 = ((m2[0] - room_center[0]) ** 2 + (m2[1] - room_center[1]) ** 2) ** 0.5

    nx, ny = (nx1, ny1) if dist1 > dist2 else (nx2, ny2)

    # Balcony rectangle
    v1 = (x1 + nx * depth, y1 + ny * depth)
    v2 = (x2 + nx * depth, y2 + ny * depth)
    return [(x1, y1), (x2, y2), v2, v1]



def plot_graph_edges_with_doors(
    edges_dict, door_edges, label_positions,
    balconies=None, attached_bathrooms=None, text_size=12, padding=5, save_path=None
):
    """Plots edges, doors, room labels, and balconies."""

    # Extract all vertices
    vertices = set()
    for edge in edges_dict.keys():
        vertices.update(edge)

    if balconies:
        for poly in balconies.values():
            vertices.update(poly)

    # Compute plot bounds
    all_x = [v[0] for v in vertices]
    all_y = [v[1] for v in vertices]
    min_x, max_x = min(all_x) - padding, max(all_x) + padding
    min_y, max_y = min(all_y) - padding, max(all_y) + padding

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_facecolor("white")

    # Plot walls (black)
    for (v1, v2) in edges_dict:
        ax.plot([v1[0], v2[0]], [v1[1], v2[1]], "k-", linewidth=4)

    # Plot balconies
    if balconies:
        for poly in balconies.values():
            x_coords = [p[0] for p in poly] + [poly[0][0]]
            y_coords = [p[1] for p in poly] + [poly[0][1]]
            ax.fill(x_coords, y_coords, color='lightgray', alpha=0.8, zorder=0)

            # Draw balcony walls (optional: use dashed gray lines to differentiate)
            for i in range(len(poly)):
                p1 = poly[i]
                p2 = poly[(i + 1) % len(poly)]
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="gray", linewidth=2, linestyle="--")
    # Plot doors (white)
    for (v1, v2) in door_edges:
        ax.plot([v1[0], v2[0]], [v1[1], v2[1]], "w-", linewidth=3)
    # Plot attached bathrooms
    if attached_bathrooms:
        for poly in attached_bathrooms.values():
            x_coords = [p[0] for p in poly] + [poly[0][0]]
            y_coords = [p[1] for p in poly] + [poly[0][1]]
            ax.fill(x_coords, y_coords, color='blue', alpha=0.2, zorder=0)

    # Plot room labels
    for label, (x, y) in label_positions.items():
        ax.text(
            x, y, label, fontsize=text_size, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
        )

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()
    plt.close()


def add_balcony_to_room(room_name, edges_dict, label_positions, balcony_depth=5.0):
    outside_edges = get_outside_edges_of_room(edges_dict, room_name)
    best_edge = pick_best_outside_edge(outside_edges)
    if not best_edge:
        print(f"No suitable outside edge found for room '{room_name}'")
        return None, None

    if room_name not in label_positions:
        print(f"Room '{room_name}' not found in label_positions for center calculation")
        return None, None

    room_center = label_positions[room_name]

    # 1. Take left (or right) portion of the edge for the balcony
    balcony_edge = create_side_segment(best_edge, fraction=0.7, from_start=True)

    # 2. Door is centered inside the balcony edge
    door_edge = create_centered_segment(balcony_edge, fraction=0.25)

    # 3. Build balcony polygon from that side
    balcony_poly = create_balcony_from_edge(balcony_edge, depth=balcony_depth, room_center=room_center)

    door_edges = {door_edge: [room_name, f"{room_name}_balcony"]}

    return {f"{room_name}_balcony": balcony_poly}, door_edges


def remove_room(graph_data, room_name):
    # Create a copy of the graph data to avoid modifying the original
    new_graph_data = {
        'vertices': graph_data['vertices'].copy(),
        'edges': graph_data['edges'].copy(),
        'room_vertices': graph_data['room_vertices'].copy()
    }

    # Identify edges that contain the room
    edges_to_remove = {edge for edge, rooms in graph_data['edges'].items() if room_name in rooms}


    # List of vertices affected
    vertices_connecting_to_deleted_room = []

    # Remove identified edges and collect affected vertices
    for edge in edges_to_remove:
        v1, v2 = edge
        print("removed edge:", new_graph_data['edges'][edge])

        # Check all vertices to see if they lie on this edge
        for vertex, rooms in graph_data['vertices'].items():
            if vertex in {v1, v2} and (vertex,rooms) not in vertices_connecting_to_deleted_room:
                for _edge, _rooms in graph_data['edges'].items():
                    if vertex in _edge and _edge != edge:
                        #print(f"The vertex {vertex} is in another edge: {_edge} of rooms {_rooms}.")
                        vertices_connecting_to_deleted_room.append((vertex, rooms))  # Store (vertex, room labels)
                        break
                

        del new_graph_data['edges'][edge]  # Remove edge
    

    for vertex, rooms in graph_data['vertices'].items():
        if room_name in rooms and (vertex, rooms) not in vertices_connecting_to_deleted_room:
            del new_graph_data['vertices'][vertex]
    
    return new_graph_data, vertices_connecting_to_deleted_room

def remove_redundant_edges(path):
    unique_edges = []
    seen_edges = set()

    for edge in path:
        edge_tuple = (edge[0][0], edge[0][1])  # ((x1, y1), (x2, y2))
        reverse_edge_tuple = (edge[0][1], edge[0][0])  # Consider undirected nature

        if edge_tuple not in seen_edges and reverse_edge_tuple not in seen_edges:
            unique_edges.append(edge)
            seen_edges.add(edge_tuple)
            seen_edges.add(reverse_edge_tuple)  # Add both directions to avoid revisiting

    return unique_edges

def plot_graph_with_path(graph_data, path, corridor_width = 35, padding=5):
    vertices = graph_data["vertices"]
    edges = graph_data["edges"]

    # Determine min and max coordinates
    all_x = [v[0] for v in vertices]
    all_y = [v[1] for v in vertices]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Apply padding
    min_x -= padding
    max_x += padding
    min_y -= padding
    max_y += padding

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    ax.set_facecolor("white")

    # Plot original graph (black edges)
    for (v1, v2) in edges:
        x_values = [v1[0], v2[0]]
        y_values = [v1[1], v2[1]]
        ax.plot(x_values, y_values, "k-", linewidth=5)  # Light black edges

    # Plot vertices (red dots)
    for vertex in vertices:
        ax.plot(vertex[0], vertex[1], "ro", markersize=4)

    for (v1, v2), _ in path:
        x_values = [v1[0], v2[0]]
        y_values = [v1[1], v2[1]]
        ax.plot(x_values, y_values, color="#00FF00", linewidth=corridor_width) 
    
    # Remove padding and save image
    plt.gca().set_position([0, 0, 1, 1])
    save_path = os.path.join(os.getcwd(), "corridor.png")  # Ensure absolute path
    plt.savefig(save_path, format="png", dpi=300, bbox_inches="tight", pad_inches=0)

    plt.show()
    plt.close()

def get_color_boundary_edges(image_path = "corridor.png"):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to RGB (OpenCV loads images in BGR format by default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Define exact green color in RGB
    target_color = np.array([0, 255, 0])  # Pure green

    # Create a mask for the exact green color
    mask = np.all(image_rgb == target_color, axis=-1).astype(np.uint8) * 255  # Convert to binary mask

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a blank image to visualize the edges
    output = np.zeros_like(image)

    # List to store boundary edges (pairs of points)
    boundary_edges = []

    # Process each contour
    for contour in contours:
        # Approximate the contour to reduce points
        epsilon = 0.001 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Convert contour points to (x, y) format and store edges
        num_points = len(approx)
        for i in range(num_points):
            v1 = tuple(approx[i][0])  # Current vertex
            v2 = tuple(approx[(i + 1) % num_points][0])  # Next vertex (wrap around to the first)

            boundary_edges.append((v1, v2))  # Store as an edge (vertex pair)

        # Draw the approximated shape
        cv2.drawContours(output, [approx], -1, (0, 255, 0), 2)

    # Display the result
    plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    plt.title("Detected Boundary Edges")
    plt.show()  # Show plot without blocking execution
    plt.close()  # Immediately close the plot window

    # Print boundary edges
    print("Detected Boundary Edges (as edges):", boundary_edges)

    return boundary_edges

def resize_graph_edges(original_graph_edges, original_size = 2400, new_size = 100):
    # Normalize edges with Y-axis flipping
    resized_graph_edges = [
        (
            (x1 / original_size * new_size, (1 - y1 / original_size) * new_size),  # Normalize and flip Y
            (x2 / original_size * new_size, (1 - y2 / original_size) * new_size)   # Normalize and flip Y
        )
        for (x1, y1), (x2, y2) in original_graph_edges
    ]

    # Print normalized edges
    print("Normalized Boundary Edges (100x100 scale):", )
    return resized_graph_edges

def merge_close_values_in_graph(edges, threshold=0.1):
    """Merge x-coordinates only with other x-coordinates and y-coordinates only with other y-coordinates."""
    
    # Collect all unique x and y values separately
    unique_x_values = set()
    unique_y_values = set()
    
    for (x1, y1), (x2, y2) in edges:
        unique_x_values.add(x1)
        unique_x_values.add(x2)
        unique_y_values.add(y1)
        unique_y_values.add(y2)

    # Sort x and y values separately
    sorted_x_values = sorted(unique_x_values)
    sorted_y_values = sorted(unique_y_values)

    # Merge close x values
    merged_x_values = {}
    merged_x_list = []

    for x in sorted_x_values:
        if merged_x_list and abs(merged_x_list[-1] - x) < threshold:
            merged_x_values[x] = merged_x_list[-1]  # Map close x values to previous value
        else:
            merged_x_list.append(x)
            merged_x_values[x] = x  # Keep the same value

    # Merge close y values
    merged_y_values = {}
    merged_y_list = []

    for y in sorted_y_values:
        if merged_y_list and abs(merged_y_list[-1] - y) < threshold:
            merged_y_values[y] = merged_y_list[-1]  # Map close y values to previous value
        else:
            merged_y_list.append(y)
            merged_y_values[y] = y  # Keep the same value

    # Replace values in edges with merged values
    new_edges = []
    for (x1, y1), (x2, y2) in edges:
        new_x1, new_y1 = merged_x_values[x1], merged_y_values[y1]
        new_x2, new_y2 = merged_x_values[x2], merged_y_values[y2]
        if new_x1 == 0:
            new_x1 = -0.1
        if new_x1 == 100:
            new_x1 = 100.1
        if new_y1 == 0:
            new_y1 = -0.1
        if new_y1 == 100:
            new_y1 = 100.1
        if new_x2 == 0:
            new_x2 = -0.1
        if new_x2 == 100:
            new_x2 = 100.1
        if new_y2 == 0:
            new_y2 = -0.1
        if new_y2 == 100:
            new_y2 = 100.1
                
        
        new_edges.append(((new_x1, new_y1), (new_x2, new_y2)))

    return new_edges

def format_corridor_edges(corridor_edges):
    """Convert corridor edges into graph format with 'corridor' label."""
    formatted_edges = {edge: ['corridor'] for edge in corridor_edges}
    return formatted_edges

def split_edges_at_intersections(edges_dict):
    """Splits all edges (room & corridor) at intersection points."""
    intersection_points = set()
    edges_list = list(edges_dict.keys())  # Convert to list for iteration

    # First pass: Find all intersections
    for i, edge1 in enumerate(edges_list):
        line1 = LineString([edge1[0], edge1[1]])

        for j, edge2 in enumerate(edges_list):
            if i >= j:
                continue  # Avoid duplicate checks

            line2 = LineString([edge2[0], edge2[1]])
            if line1.intersects(line2):
                intersection = line1.intersection(line2)

                if intersection.geom_type == "Point":
                    intersection_points.add((intersection.x, intersection.y))
                elif intersection.geom_type == "MultiPoint":
                    for pt in intersection.geoms:
                        intersection_points.add((pt.x, pt.y))

    # Second pass: Split all edges at the found intersections
    new_edges = {}
    for edge, labels in edges_dict.items():
        sorted_points = sorted([edge[0], edge[1]] + [pt for pt in intersection_points if LineString(edge).contains(Point(pt))])

        for k in range(len(sorted_points) - 1):
            new_edges[(sorted_points[k], sorted_points[k + 1])] = labels  # Preserve original labels

    return new_edges

def remove_duplicate_edges(edges_to_filter):
    duplicate_edges = {}
    unique_edges = {}
    for key,value in edges_to_filter.items():
        if key[0] == key[1]:
            duplicate_edges[key] = value
        else:
            unique_edges[key] = value
    return unique_edges

def construct_corridor_polygon(corridor_edges):
    """Construct a valid corridor polygon by ordering edges correctly."""
    G = nx.Graph()
    
    # Build graph of connected edges
    for edge in corridor_edges:
        G.add_edge(edge[0], edge[1])
    
    # Find a cycle (loop) in the graph
    cycle = list(nx.find_cycle(G, orientation="ignore"))

    # Extract ordered points from the cycle
    ordered_vertices = [cycle[0][0]] + [edge[1] for edge in cycle]
    
    # Create a valid polygon
    return Polygon(ordered_vertices)

def get_room_edges_within_corridor(corridor_edges, room_edges):
    """Find room edges that are enclosed by the corridor polygon."""
    enclosed_edges = {}

    # Construct the correct corridor polygon
    corridor_polygon = construct_corridor_polygon(corridor_edges)

    # Check which room edges are fully inside the corridor
    for edge, rooms in room_edges.items():
        edge_line = LineString([edge[0], edge[1]])

        if corridor_polygon.contains(edge_line):  # Ensure the entire edge is inside
            for room in rooms:
                if room not in enclosed_edges:
                    enclosed_edges[room] = []
                enclosed_edges[room].append(edge)

    return enclosed_edges, corridor_polygon

def get_room_and_corridor_edges(room_and_corridor_edges_dict):
    room_edges = {}
    corridor_edges = {}

    for key, value in room_and_corridor_edges_dict.items():
        if 'corridor' in value:
            corridor_edges[key] = value
        else:
            room_edges[key] = value
    return corridor_edges, room_edges

def construct_room_polygons(room_edges):
    """Construct valid polygons for each room using ordered edges."""
    room_polygons = {}

    # Organize edges by room
    room_edges_dict = {}
    for edge, rooms in room_edges.items():
        for room in rooms:
            if room not in room_edges_dict:
                room_edges_dict[room] = []
            room_edges_dict[room].append(edge)

    # Construct polygons for each room
    for room, edges in room_edges_dict.items():
        G = nx.Graph()
        for edge in edges:
            G.add_edge(edge[0], edge[1])

        # Check if the graph is connected before finding a cycle
        if not nx.is_connected(G):
            print(f"Warning: Room '{room}' edges do not form a complete closed shape. Skipping...")
            continue

        try:
            # Find a cycle (closed loop) in the room edges
            cycle = list(nx.find_cycle(G, orientation="ignore"))
            ordered_vertices = [cycle[0][0]] + [edge[1] for edge in cycle]

            # Create polygon and store
            room_polygons[room] = Polygon(ordered_vertices)
        except nx.exception.NetworkXNoCycle:
            print(f"Warning: No cycle found for room '{room}'. Skipping...")

    return room_polygons

def get_corridor_edges_within_rooms(room_edges, corridor_edges):
    """Find corridor edges that fall within room polygons."""
    room_polygons = construct_room_polygons(room_edges)
    corridor_in_rooms = {}

    for corridor_edge, _ in corridor_edges.items():
        edge_line = LineString([corridor_edge[0], corridor_edge[1]])

        for room, room_polygon in room_polygons.items():
            if room_polygon.contains(edge_line):  # Check if edge is fully inside
                if room not in corridor_in_rooms:
                    corridor_in_rooms[room] = []
                corridor_in_rooms[room].append(corridor_edge)

    return corridor_in_rooms

def remove_given_edges(graph_edges, edges_to_remove):
    """Removes given edges from a given dictionary of edges."""
    
    # Collect all edges from edges_to_remove into a set
    edges_set = set()
    for edges in edges_to_remove.values():
        edges_set.update(edges)

    # Remove edges from unique_edges if they exist in corridor_edges
    filtered_edges = {edge: labels for edge, labels in graph_edges.items() if edge not in edges_set}

    return filtered_edges

def remove_corridor_edges_from_living_room(graph_edges, edges_to_remove):
    """Removes given edges from a given dictionary of edges."""
    
    # Collect all edges from edges_to_remove into a set
    edges_set = []
    for key, value in edges_to_remove.items():
        if key == "livingroom_1":
           for edge in value:
            edges_set.append(edge)
           print(len(edges_set))

    filtered_edges = {edge: labels for edge, labels in graph_edges.items() if edge not in edges_set}

    return filtered_edges

def get_adjacency_requirements(user_constraints, room_sizes):
    valid_room_names = list(room_sizes.keys())
    adjacency_raw = user_constraints["floorplan_relationships"]["adjacentTo"]
    mapped_adjacency = []

    def normalize_room_name(original_name):
        cleaned_name = original_name.replace("_", "").lower()

        if cleaned_name in room_sizes:
            return original_name

        closest_match = find_closest_room(cleaned_name, valid_room_names)

        # Extract numeric suffix (if any)
        suffix_match = re.search(r'\d+$', original_name)
        suffix = f"_{suffix_match.group()}" if suffix_match else ""

        return closest_match + suffix

    for room1, room2 in adjacency_raw:
        mapped_room1 = normalize_room_name(room1)
        mapped_room2 = normalize_room_name(room2)
        mapped_adjacency.append([mapped_room1, mapped_room2])

    return mapped_adjacency

def count_satisfied_adjacencies(room_data, adjacency_requirements):
    """Counts how many adjacency requirements are satisfied."""
    satisfied_count = 0
    for room1_label, room2_label in adjacency_requirements:
        # Find the room indices
        room1_idx = next((i for i, r in room_data.items() if r['label'] == room1_label), None)
        room2_idx = next((i for i, r in room_data.items() if r['label'] == room2_label), None)

        if room1_idx is not None and room2_idx is not None:
            # Check if room1 and room2 are adjacent
            if room2_idx in room_data[room1_idx]['adjacent_rooms']:
                satisfied_count += 1

    return satisfied_count

def optimize_adjacency(room_data, adjacency_requirements):
    """Attempts to maximize adjacency satisfaction by swapping rooms."""
    best_room_data = copy.deepcopy(room_data)
    best_score = count_satisfied_adjacencies(room_data, adjacency_requirements)
    best_pair = None

    swappable_pairs = get_swappable_rooms(room_data)

    for pair in swappable_pairs:
        swapped_room_data = swap_rooms(room_data, pair)
        new_score = count_satisfied_adjacencies(swapped_room_data, adjacency_requirements)

        print(f"Trying swap {pair}: Score = {new_score}")

        if new_score > best_score:
            best_score = new_score
            best_room_data = swapped_room_data
            best_pair = pair

    if best_pair is not None:
        i, j = best_pair
        print(f"\n✅ Best swap: {best_pair} — New Score: {best_score}")
        print(f"Swapped room '{room_data[i]['label']}' with '{room_data[j]['label']}'")
        print(f"New positions:")
        print(f"{best_room_data[i]['label']}: {best_room_data[i]['rect']}")
        print(f"{best_room_data[j]['label']}: {best_room_data[j]['rect']}")
    else:
        print("\n⚠️ No beneficial swap found.")

    return best_room_data, best_score


def generate_door_edges(edges_dict, door_size=4, offset_threshold=1):
    door_edges = {}
    added_doors = set()  # Track label combinations with doors

    for (start, end), labels in edges_dict.items():
        if len(labels) > 1:  # Only process shared edges
            label_key = frozenset(labels)  # Order-independent tracking

            if label_key in added_doors:
                continue  # Skip if a door has already been added for this label pair

            x1, y1 = start
            x2, y2 = end
            
            # Determine if the edge is horizontal or vertical
            if x1 == x2:  # Vertical edge
                edge_length = abs(y2 - y1)
                if edge_length > door_size + offset_threshold * 2:
                    min_door_start = y1 + offset_threshold
                    max_door_start = y2 - door_size - offset_threshold
                    door_start = random.uniform(min_door_start, max_door_start)
                    
                    door_end = door_start + door_size
                    door_edges[((x1, door_start), (x2, door_end))] = labels
                    added_doors.add(label_key)

            elif y1 == y2:  # Horizontal edge
                edge_length = abs(x2 - x1)
                if edge_length > door_size + offset_threshold * 2:
                    min_door_start = x1 + offset_threshold
                    max_door_start = x2 - door_size - offset_threshold
                    door_start = random.uniform(min_door_start, max_door_start)
                    
                    door_end = door_start + door_size
                    door_edges[((door_start, y1), (door_end, y2))] = labels
                    added_doors.add(label_key)

    return door_edges

def get_room_edges_with_corridor_connection(corridor_edges_in_rooms, updated_edges_removed_corridor_from_living_room):
    updated_corridor_edges_in_rooms = {}
    # removing corridor edges enclosed in the living room.
    for key, value in corridor_edges_in_rooms.items():
        if key != 'livingroom_1':
            updated_corridor_edges_in_rooms[key] = value

    room_edges_with_corridor_connection = copy.deepcopy(updated_edges_removed_corridor_from_living_room)

    for key, value in updated_corridor_edges_in_rooms.items():
        for edge in value:
            label = [key, 'corridor']
            room_edges_with_corridor_connection[edge] = label
    return room_edges_with_corridor_connection

def get_room_label_positions(room_data, grid_size=100):
    """Returns the center positions (x, y) for placing room labels in a 100x100 grid."""
    label_positions = {}

    for room_id, room in room_data.items():
        rect = room['rect']

        # Calculate the center of the room
        center_x = rect['x'] + rect['dx'] / 2
        center_y = rect['y'] + rect['dy'] / 2

        # Scale to fit the 100x100 grid
        scaled_x = (center_x / 100) * grid_size
        scaled_y = (center_y / 100) * grid_size

        # Store position with room label
        label_positions[room['label']] = (scaled_x, scaled_y)

    return label_positions

def get_disconnected_rooms(room_data):
    # Step 1: Find the living room ID
    living_room_id = None
    for room_id, room_info in room_data.items():
        if "livingroom" in room_info['label'].lower():
            living_room_id = room_id
            break

    # Step 2: Get adjacent rooms to the living room
    adjacent_to_livingroom = set(room_data[living_room_id]['adjacent_rooms']) if living_room_id is not None else set()

    # Step 3: Find disconnected rooms
    disconnected_rooms = []
    for room_id, room_info in room_data.items():
        if room_id != living_room_id and room_id not in adjacent_to_livingroom:
            disconnected_rooms.append(room_info['label'])

    return disconnected_rooms