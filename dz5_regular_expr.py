"""
решить задачу синтеза конечного автомата по заданному регулярному выражению R.

R = (a∪b∪c).
R = abc

показать ход решения в коде
сделать графика графа
сделать талицу переходов

Для начала определим конечные автоматы для каждого регулярного выражения.

Для �=(�∪�∪�)∗R=(a∪b∪c)∗: Это регулярное выражение описывает все возможные строки, состоящие из символов �,�,a,b, и �c, включая пустую строку. Для такого автомата нам нужно всего одно состояние, которое также будет начальным и конечным. С этого состояния будут исходить три перехода по символам �,�,a,b, и �c обратно в это же состояние.

Для �=�∗�∗�∗R=a∗b∗c∗: Это регулярное выражение описывает строки, которые начинаются с нуля или более символов �a, за которыми следует ноль или более символов �b, и заканчиваются нулем или более символами �c. Здесь нам потребуются четыре состояния:

Состояние 1 (начальное и конечное): переход по �a ведет обратно в состояние 1, переход по �b ведет в состояние 2.

Состояние 2 (конечное): переход по �b ведет обратно в состояние 2, переход по �c ведет в состояние 3.

Состояние 3 (конечное): переход по �c ведет обратно в состояние 3.

Все другие переходы ведут в "мусорное" состояние 4, из которого нет выхода.

Теперь приступим к реализации и построению графиков для каждого автомата.
"""

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# Define automata for each regular expression

# For R = (a∪b∪c)*
G1 = nx.MultiDiGraph()
G1.add_nodes_from([1])
G1.add_edges_from([(1, 1, {'label': 'a'}), (1, 1, {'label': 'b'}), (1, 1, {'label': 'c'})])

# For R = a*b*c*
G2 = nx.MultiDiGraph()
G2.add_nodes_from([1, 2, 3, 4])  
G2.add_edges_from([(1, 1, {'label': 'a'}), (1, 2, {'label': 'b'}), 
                   (2, 2, {'label': 'b'}), (2, 3, {'label': 'c'}),
                   (3, 3, {'label': 'c'}), 
                   (1, 4, {'label': 'c'}), (2, 4, {'label': 'a'}), (3, 4, {'label': 'a,b'})])

# Function to display edge labels
def draw_edge_labels(G, pos, ax, labels):
    for (u, v, key), label in labels.items():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        x, y = x1 * 0.6 + x2 * 0.4, y1 * 0.6 + y2 * 0.4  
        ax.text(x, y, label, horizontalalignment='center', verticalalignment='center')

# Positions for automaton nodes
pos1 = {1: (0, 0)}
pos2 = {1: (0, 0), 2: (1, 1), 3: (1, -1), 4: (2, 0)}

# Fetch edge labels
labels1 = nx.get_edge_attributes(G1, 'label')
labels2 = nx.get_edge_attributes(G2, 'label')

# Draw automata
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# For R = (a∪b∪c)*
axs[0].set_title("Automaton for R = (a∪b∪c)*")
nx.draw(G1, pos1, with_labels=True, node_size=2000, node_color='skyblue', edge_color='black', font_size=15, ax=axs[0])
draw_edge_labels(G1, pos1, axs[0], labels1)

# For R = a*b*c*
axs[1].set_title("Automaton for R = a*b*c*")
nx.draw(G2, pos2, with_labels=True, node_size=2000, node_color='skyblue', edge_color='black', font_size=15, ax=axs[1])
draw_edge_labels(G2, pos2, axs[1], labels2)

plt.tight_layout()
plt.show()

# Transition tables
transition_table_1 = {
    "State": [1],
    "a": [1],
    "b": [1],
    "c": [1]
}

transition_table_2 = {
    "State": [1, 2, 3, 4],
    "a": [1, 4, 4, 4],
    "b": [2, 2, 4, 4],
    "c": [4, 3, 3, 4]
}

df1 = pd.DataFrame(transition_table_1)
df2 = pd.DataFrame(transition_table_2)

df1, df2