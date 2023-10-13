import networkx as nx
import matplotlib.pyplot as plt

# Определение переходов для языка L
L_transitions = {
    'q0': {'a': 'q0', 'b': 'q1', 'c': 'q2'},
    'q1': {'a': 'q2', 'b': 'q1'},
    'q2': {'b': 'q1'},
}

def construct_L3_automaton(transitions, final_states_option):
    # Шаг 1: Определение нового набора состояний для L^3
    L3_states = {(s1, s2, s3) for s1 in transitions for s2 in transitions for s3 in transitions}
    
    L3_transitions = {}
    for state in L3_states:
        L3_transitions[state] = {}
        # Для каждого символа в языке L определяем переходы для L^3
        for symbol in transitions[state[0]]:
            if symbol in transitions[state[1]] and symbol in transitions[state[2]]:
                next_state = (transitions[state[0]][symbol], transitions[state[1]][symbol], transitions[state[2]][symbol])
                L3_transitions[state][symbol] = next_state
    
    # Начальное состояние для L^3 - это тройка из начального состояния L
    L3_initial_state = ('q0', 'q0', 'q0')
    
    # Определение заключительных состояний для L^3
    final_states_list = list(final_states_option)
    L3_final_states = {(s1, s2, s3) for s1 in final_states_list for s2 in final_states_list for s3 in final_states_list}
    
    return L3_transitions, L3_initial_state, L3_final_states

# Определение заключительных состояний для автомата
final_state_options = [
    ({"q1"}),
    ({"q0", "q2"})
]

# Построение автомата для L^3 для каждого набора заключительных состояний
L3_automata = [construct_L3_automaton(L_transitions, final_states_option) for final_states_option in final_state_options]

def plot_automaton(transitions, final_states_set):
    # Инициализация графа для визуализации автомата
    G = nx.DiGraph()

    # Добавление вершин и рёбер в граф
    for state, transitions_dict in transitions.items():
        for symbol, next_state in transitions_dict.items():
            G.add_edge(state, next_state, label=symbol)

    # Визуализация графа
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))

    non_final_states = set(transitions.keys()) - final_states_set
    nx.draw_networkx_nodes(G, pos, nodelist=final_states_set, node_color='lightblue', node_size=700, label="Заключительные состояния")
    nx.draw_networkx_nodes(G, pos, nodelist=non_final_states, node_color='lightgray', node_size=700, label="Остальные состояния")
    nx.draw_networkx_edges(G, pos)
    edge_labels = {(u, v): G[u][v]['label'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(G, pos)

    plt.legend()
    plt.title("Автомат для L^3")
    plt.axis('off')
    plt.show()

# Визуализация автомата для L^3 для каждого набора заключительных состояний
for L3_transitions, _, L3_final_states in L3_automata:
    plot_automaton(L3_transitions, L3_final_states)
