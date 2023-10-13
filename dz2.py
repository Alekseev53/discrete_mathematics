import networkx as nx
import matplotlib.pyplot as plt

# Инициализация автоматов
L1_transitions = {
    'q0': {'1': 'q0', '0': 'q1'},
    'q1': {'1': 'q0', '0': 'q2'},
    'q2': {'1': 'q1', '0': 'q0'}
}
L1_final = {'q2'}

L2_transitions = {
    'q0': {'1': 'q1', '0': 'q2'},
    'q1': {'1': 'q0', '0': 'q2'}
}
L2_final = {'q0'}

L_intersection_transitions = {}
L_union_transitions = {}
L_intersection_final = set()
L_union_final = set()

# Вычисляем переходы и конечные состояния для результирующих автоматов
for state1 in L1_transitions:
    for state2 in L2_transitions:
        combined_state = (state1, state2)
        
        L_intersection_transitions[combined_state] = {}
        L_union_transitions[combined_state] = {}
        
        for symbol in L1_transitions[state1]:
            if symbol in L2_transitions[state2]:
                next_state1 = L1_transitions[state1][symbol]
                next_state2 = L2_transitions[state2][symbol]
                combined_next_state = (next_state1, next_state2)
                
                L_intersection_transitions[combined_state][symbol] = combined_next_state
                L_union_transitions[combined_state][symbol] = combined_next_state
                
                # Проверка на конечные состояния
                if next_state1 in L1_final and next_state2 in L2_final:
                    L_intersection_final.add(combined_next_state)
                if next_state1 in L1_final or next_state2 in L2_final:
                    L_union_final.add(combined_next_state)

def draw_automaton(transitions, final_states, title):
    G = nx.MultiDiGraph()
    
    for state in transitions:
        for symbol, next_state in transitions[state].items():
            G.add_edge(state, next_state, label=symbol)
    
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 8))
    
    node_colors = ["green" if node in final_states else "red" for node in G.nodes()]
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500, font_size=15)
    
    edge_labels = {(u, v): G[u][v][0]['label'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=15)
    
    plt.title(title)
    plt.show()

# Визуализация автоматов пересечения и объединения
draw_automaton(L_intersection_transitions, L_intersection_final, "Автомат пересечения (L1 И L2)")
draw_automaton(L_union_transitions, L_union_final, "Автомат объединения (L1 ИЛИ L2)")

import pandas as pd

# Преобразование переходов в табличный формат
def transitions_to_table(transitions):
    table_data = []
    
    for state, transition in transitions.items():
        row = {'State': state}
        for symbol, next_state in transition.items():
            row[symbol] = next_state
        table_data.append(row)
        
    return pd.DataFrame(table_data).fillna('-')

# Получение таблиц для автоматов пересечения и объединения
intersection_table = transitions_to_table(L_intersection_transitions)
union_table = transitions_to_table(L_union_transitions)

print(intersection_table, union_table)
