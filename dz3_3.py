from collections import deque
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

# Define the transition diagrams for L1
L1_transitions = {
    'q0': {'1': 'q0', '0': 'q2'},
    'q1': {'1': 'q0', '0': 'q3'},
    'q2': {'1': 'q1', '0': 'q3'},
    'q3': {'1': 'q3', '0': 'q0'},
}

def construct_L_star_automaton(transitions, final_states_option):
    L_star_transitions = transitions.copy()
    
    # Add epsilon-like transitions from every final state to the initial state
    for final_state in final_states_option:
        if 'ε' in L_star_transitions[final_state]:
            L_star_transitions[final_state]['ε'].append('q0')
        else:
            L_star_transitions[final_state]['ε'] = ['q0']

    # The initial state becomes a final state
    final_states_option.add('q0')
    
    return L_star_transitions, final_states_option

def plot_L_star_automaton(transitions, final_states_set):
    G = nx.DiGraph()

    for state, transitions_dict in transitions.items():
        for symbol, next_states in transitions_dict.items():
            if not isinstance(next_states, list):
                next_states = [next_states]
            for next_state in next_states:
                G.add_edge(state, next_state, label=symbol)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))

    # Draw nodes
    non_final_states = set(transitions.keys()) - final_states_set
    nx.draw_networkx_nodes(G, pos, nodelist=final_states_set, node_color='lightblue', node_size=700, label="Final States")
    nx.draw_networkx_nodes(G, pos, nodelist=non_final_states, node_color='lightgray', node_size=700, label="Non-final States")

    # Draw edges
    nx.draw_networkx_edges(G, pos)

    # Draw labels
    edge_labels = {(u, v): G[u][v]['label'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(G, pos)

    plt.legend()
    plt.title("Automaton for L*")
    plt.axis('off')
    plt.show()

# Define the final state options
final_state_options = [
    ({"q1","q3"}),
    ({"q0", "q2"}),
    ({"q2", "q3"})
]

# Constructing and plotting the automaton for L* for each set of final states
for final_states_option in final_state_options:
    L_star_transitions, L_star_final_states = construct_L_star_automaton(L1_transitions, set(final_states_option))
    plot_L_star_automaton(L_star_transitions, L_star_final_states)
