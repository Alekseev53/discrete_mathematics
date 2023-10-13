import networkx as nx
import matplotlib.pyplot as plt

# Определение переходов для языков L1 и L2
L1_transitions = {
    'q0': {'1': 'q0', '0': 'q1'},
    'q1': {'1': 'q0', '0': 'q2'},
    'q2': {'1': 'q1', '0': 'q0'}
}

L2_transitions = {
    'q0': {'1': 'q1', '0': 'q2'},
    'q1': {'1': 'q2', '0': 'q1'},
    'q2': {'1': 'q0', '0': 'q2'},
}

# Построение произведения автоматов для L1 и L2
def construct_product_automaton(transitions1, transitions2):
    product_transitions = {}
    
    # Для каждого состояния в L1 и каждого состояния в L2 создаем новое состояние в произведении
    for state1 in transitions1:
        for state2 in transitions2:
            product_state = (state1, state2)
            product_transitions[product_state] = {}
            
            # Определение переходов для нового состояния
            for symbol, next_state1 in transitions1[state1].items():
                next_state2 = transitions2[state2][symbol]
                product_transitions[product_state][symbol] = (next_state1, next_state2)
                
    return product_transitions

product_transitions = construct_product_automaton(L1_transitions, L2_transitions)

# Определение заключительных состояний для произведения
final_state_options = [
    ({"q1", "q2"}, {"q2"}),
    ({"q0", "q2"}, {"q1"}),
    ({"q0"}, {"q0", "q2"})
]

product_final_states = []

# Определение заключительных состояний для каждой комбинации
for final_states1, final_states2 in final_state_options:
    final_states_product = {(state1, state2) for state1 in final_states1 for state2 in final_states2}
    product_final_states.append(final_states_product)

# Визуализация автомата
def plot_automaton(transitions, final_states_set):
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
    plt.title("Product Automaton")
    plt.axis('off')
    plt.show()

# Plotting the product automaton for each set of final states
for final_states in product_final_states:
    plot_automaton(product_transitions, final_states)

