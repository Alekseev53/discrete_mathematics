import networkx as nx
import matplotlib.pyplot as plt

# Функция для минимизации автомата
def minimize_automaton(transitions, start_state, final_states):
    """
    Минимизация автомата с использованием разбиения эквивалентных состояний.
    """
    # Начальное разбиение: конечные состояния и не конечные состояния
    partitions = [set(final_states), set(transitions.keys()) - set(final_states)]
    
    changed = True
    while changed:
        changed = False
        
        # Новые разбиения после учета переходов
        new_partitions = []
        
        for partition in partitions:
            # Группировка состояний по их переходам
            transition_groups = {}
            for state in partition:
                # Создание ключа, представляющего переходы для состояния
                key = tuple((input_symbol, transitions[state][input_symbol]) for input_symbol in transitions[state])
                if key not in transition_groups:
                    transition_groups[key] = []
                transition_groups[key].append(state)
            
            # Если разбиение разделено, пометить changed как True
            if len(transition_groups) > 1:
                changed = True
            for group in transition_groups.values():
                new_partitions.append(set(group))
        
        partitions = new_partitions
        
    # Создание минимизированного автомата
    min_G = nx.DiGraph()
    for group in partitions:
        min_G.add_node(tuple(group))
        
        # Добавление рёбер
        for input_symbol in transitions[next(iter(group))]:
            target_state = transitions[next(iter(group))][input_symbol]
            target_group = next(filter(lambda x: target_state in x, partitions), None)
            if target_group:
                min_G.add_edge(tuple(group), tuple(target_group), label=input_symbol)

    return min_G

# Функция для отображения графа
def display_graph(G, title=""):
    """Функция для визуализации графа."""
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=15, width=2, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): G[u][v]['label'] for u, v in G.edges()}, font_size=15)
    plt.title(title)
    plt.show()

# Создаем новый направленный граф
DFA = nx.DiGraph()

# Определяем наши состояния и входной алфавит
states = [('even', 0), ('even', 1), ('even', 2), ('odd', 0), ('odd', 1), ('odd', 2)]
alphabet = ['1', '2', '3']

# Определяем начальное состояние и принимающие состояния
start_state = ('odd', 1)
accept_states = [('even', 0)]

# Заполняем DFA ребрами на основе нашей функции перехода
transitions = {}
for state in states:
    parity, mod3 = state
    for symbol in alphabet:
        new_number = int(symbol)
        new_parity = 'even' if new_number % 2 == 0 else 'odd'
        new_mod3 = (mod3 + new_number) % 3
        new_state = (new_parity, new_mod3)
        
        DFA.add_edge(state, new_state, label=symbol)
        transitions[(state, symbol)] = new_state

# Визуализируем DFA
pos = nx.spring_layout(DFA)
plt.figure(figsize=(10, 8))

nx.draw_networkx_nodes(DFA, pos, node_color="lightblue")
nx.draw_networkx_edges(DFA, pos, connectionstyle="arc3,rad=0.1")
nx.draw_networkx_labels(DFA, pos)

# Добавляем метки к ребрам
edge_labels = {(u, v): DFA[u][v]['label'] for u, v in DFA.edges()}
nx.draw_networkx_edge_labels(DFA, pos, edge_labels=edge_labels, label_pos=0.4)

# Выделяем начальное состояние и принимающие состояния
nx.draw_networkx_nodes(DFA, pos, nodelist=[start_state], node_color="green")
nx.draw_networkx_nodes(DFA, pos, nodelist=accept_states, node_color="yellow")

plt.title("DFA для чисел, кратных 6, на {1,2,3}")
plt.axis('off')
plt.show()
