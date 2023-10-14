import networkx as nx
import matplotlib.pyplot as plt

# Создание графа автомата
G = nx.DiGraph()

# Добавление состояний (вершин графа)
states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
G.add_nodes_from(states)

# Добавление переходов (рёбер графа) на основе таблицы переходов
transitions = {
    'q0': {'0': 'q1', '1': 'q2'},
    'q1': {'0': 'q4', '1': 'q5'},
    'q2': {'0': 'q0', '1': 'q0'},
    'q3': {'0': 'q5', '1': 'q4'},
    'q4': {'0': 'q3', '1': 'q5'},
    'q5': {'0': 'q3', '1': 'q4'}
}
for state, transition in transitions.items():
    for input_symbol, next_state in transition.items():
        G.add_edge(state, next_state, label=input_symbol)

# Отображение графа
pos = nx.spring_layout(G)
plt.figure(figsize=(10, 8))

nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=15, width=2, edge_color='gray')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): G[u][v]['label'] for u, v in G.edges()}, font_size=15)

plt.title("Автомат на основе таблицы переходов")
plt.show()

def minimize_automaton(G, start_state, final_states):
    """
    Minimize the automaton using the partitioning of equivalent states.
    """
    # Initial partition: Final states and non-final states
    partitions = [set(final_states), set(G.nodes()) - set(final_states)]
    
    changed = True
    while changed:
        changed = False
        
        # New partitions after considering transitions
        new_partitions = []
        
        for partition in partitions:
            # Group states by their transitions
            transition_groups = {}
            for state in partition:
                # Generate a key representing the transitions for the state
                key = tuple((input_symbol, transitions[state][input_symbol]) for input_symbol in transitions[state])
                if key not in transition_groups:
                    transition_groups[key] = []
                transition_groups[key].append(state)
            
            # If a partition is split, mark changed as True
            if len(transition_groups) > 1:
                changed = True
            for group in transition_groups.values():
                new_partitions.append(set(group))
        
        partitions = new_partitions
        
    # Creating the minimized automaton
    min_G = nx.DiGraph()
    for group in partitions:
        min_G.add_node(tuple(group))
        
        # Adding edges
        for input_symbol in transitions[next(iter(group))]:
            target_state = transitions[next(iter(group))][input_symbol]
            target_group = next(filter(lambda x: target_state in x, partitions), None)
            if target_group:
                min_G.add_edge(tuple(group), tuple(target_group), label=input_symbol)

    return min_G

# Minimizing the automaton for condition а)
min_G_a = minimize_automaton(G, 'q0', ['q4', 'q5'])

def display_graph(G, title=""):
    """Utility function to display a graph."""
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=15, width=2, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): G[u][v]['label'] for u, v in G.edges()}, font_size=15)
    plt.title(title)
    plt.show()

# Displaying the minimized automaton for condition а)
display_graph(min_G_a, "Minimized Automaton for Condition а)")
