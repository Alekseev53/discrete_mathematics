import networkx as nx
import matplotlib.pyplot as plt

# Определение переходов для языка L1
L1_transitions = {
    'q0': {'1': 'q0', '0': 'q2'},
    'q1': {'1': 'q0', '0': 'q3'},
    'q2': {'1': 'q1', '0': 'q3'},
    'q3': {'1': 'q3', '0': 'q0'},
}

def construct_L_star_automaton(transitions, final_states_option):
    # Копирование переходов из оригинального автомата
    L_star_transitions = transitions.copy()
    
    # Добавление эпсилон-переходов из каждого заключительного состояния в начальное
    for final_state in final_states_option:
        if 'ε' not in L_star_transitions[final_state]:
            L_star_transitions[final_state]['ε'] = []
        L_star_transitions[final_state]['ε'].append('q0')

    # Начальное состояние становится заключительным
    final_states_option.add('q0')
    
    return L_star_transitions, final_states_option

def plot_L_star_automaton(transitions, final_states_set):
    # Инициализация графа
    G = nx.DiGraph()

    # Добавление вершин и рёбер в граф
    for state, transitions_dict in transitions.items():
        for symbol, next_states in transitions_dict.items():
            if not isinstance(next_states, list):
                next_states = [next_states]
            for next_state in next_states:
                G.add_edge(state, next_state, label=symbol)

    # Визуализация графа
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))

    non_final_states = set(transitions.keys()) - final_states_set
    nx.draw_networkx_nodes(G, pos, nodelist=final_states_set, node_color='lightblue', node_size=700, label="Заключительные состояния")
    nx.draw_networkx_nodes(G, pos, nodelist=non_final_states, node_color='lightgray', node_size=700, label="Не заключительные состояния")
    nx.draw_networkx_edges(G, pos)
    edge_labels = {(u, v): G[u][v]['label'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(G, pos)

    plt.legend()
    plt.title("Автомат для L*")
    plt.axis('off')
    plt.show()

# Заключительные состояния
final_state_options = [
    ({"q1","q3"}),
    ({"q0", "q2"}),
    ({"q2", "q3"})
]

# Построение и визуализация автомата для L* для каждого набора заключительных состояний
for final_states_option in final_state_options:
    L_star_transitions, L_star_final_states = construct_L_star_automaton(L1_transitions, set(final_states_option))
    plot_L_star_automaton(L_star_transitions, L_star_final_states)
