from collections import deque
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

# NFA transitions
nfa_transitions = {
    'q': {'a': {'q'}, 'b': {'q1'}},
    'q1': {'a': {'q1', 'q2'}, 'b': {'q'}},
    'q2': {'a': {'q3'}, 'b': {'q2'}},
    'q3': {'a': {'q1'}, 'b': {'q3'}}
}

# Re-initialize DFA states and transitions
dfa_states = set()
dfa_transitions = {}
new_states = deque([frozenset({'q'})])  # start with the start state of the NFA

# Discover states of the DFA
while new_states:
    current_state = new_states.popleft()  # get the next state
    dfa_states.add(current_state)  # add it to the states of the DFA
    
    # initialize transition for current state
    dfa_transitions[current_state] = {}
    
    for symbol in ['a', 'b']:  # for each input symbol
        # compute the transition for current state and symbol
        next_state = frozenset().union(*[nfa_transitions[q][symbol] for q in current_state if symbol in nfa_transitions[q]])
        dfa_transitions[current_state][symbol] = next_state
        
        # if this is a new state, add it to the queue to be processed
        if next_state and next_state not in dfa_states:
            new_states.append(next_state)

# Output the discovered DFA states and transitions
print("DFA States:")
pprint(dfa_states)

# Output the discovered DFA transitions
print("\nDFA Transitions:")
pprint(dfa_transitions)

# Convert frozenset to string representation
def state_to_str(state):
    return ','.join(sorted(state))

# Update nodes and edges with the new representation
G = nx.DiGraph()

# Add nodes for each state in the DFA
for state in dfa_states:
    G.add_node(state_to_str(state))

# Add edges based on the transitions in the DFA
for state, transitions in dfa_transitions.items():
    for symbol, next_state in transitions.items():
        G.add_edge(state_to_str(state), state_to_str(next_state), label=symbol)

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=1500, node_color='skyblue', font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): G[u][v]['label'] for u, v in G.edges()}, font_color='red')

plt.title("DFA Visualization (Simplified)")
plt.show()
