from collections import deque
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

# Переходы NFA
nfa_transitions = {
    'q': {'a': {'q'}, 'b': {'q1'}},
    'q1': {'a': {'q1', 'q2'}, 'b': {'q'}},
    'q2': {'a': {'q3'}, 'b': {'q2'}},
    'q3': {'a': {'q1'}, 'b': {'q3'}}
}

# Переинициализация состояний и переходов DFA
dfa_states = set()
dfa_transitions = {}
new_states = deque([frozenset({'q'})])  # начинаем с начального состояния NFA

# Определяем состояния DFA
while new_states:
    current_state = new_states.popleft()  # берем следующее состояние
    dfa_states.add(current_state)  # добавляем его в состояния DFA
    
    # инициализируем переход для текущего состояния
    dfa_transitions[current_state] = {}
    
    for symbol in ['a', 'b']:  # для каждого входного символа
        # вычисляем переход для текущего состояния и символа
        next_state = frozenset().union(*[nfa_transitions[q][symbol] for q in current_state if symbol in nfa_transitions[q]])
        dfa_transitions[current_state][symbol] = next_state
        
        # если это новое состояние, добавляем его в очередь для обработки
        if next_state and next_state not in dfa_states:
            new_states.append(next_state)

# Выводим обнаруженные состояния DFA и переходы
print("Состояния DFA:")
pprint(dfa_states)

# Выводим обнаруженные переходы DFA
print("\nПереходы DFA:")
pprint(dfa_transitions)

# Преобразование frozenset в строковое представление
def state_to_str(state):
    return ','.join(sorted(state))

# Обновляем узлы и ребра с новым представлением
G = nx.DiGraph()

# Добавляем узлы для каждого состояния в DFA
for state in dfa_states:
    G.add_node(state_to_str(state))

# Добавляем ребра на основе переходов в DFA
for state, transitions in dfa_transitions.items():
    for symbol, next_state in transitions.items():
        G.add_edge(state_to_str(state), state_to_str(next_state), label=symbol)

# Рисуем граф
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=1500, node_color='skyblue', font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): G[u][v]['label'] for u, v in G.edges()}, font_color='red')

plt.title("Визуализация DFA (Упрощенная)")
plt.show()
