def dijkstra_shortest_path(g, start_vertex):
    # Put all vertices in an unvisited queue.
    unvisited_queue = []
    for current_vertex in g.adjacency_list:
        unvisited_queue.append(current_vertex)

    # Start_vertex has a distance of 0 from itself
    start_vertex.distance = 0

    # One vertex is removed with each iteration; repeat until the list is
    # empty.
    while len(unvisited_queue) > 0:

        # Visit vertex with minimum distance from start_vertex
        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_queue.pop(smallest_index)

        # Check potential path lengths from the current vertex to all neighbors.
        for adj_vertex in g.adjacency_list[current_vertex]:
            edge_weight = g.edge_weights[(current_vertex, adj_vertex)]
            alternative_path_distance = current_vertex.distance + edge_weight

            # If shorter path from start_vertex to adj_vertex is found,
            # update adj_vertex's distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex
