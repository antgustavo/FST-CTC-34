class LevenshteinAutomaton:
    def __init__(self, string, n):
        self.string = string
        self.max_edits = n

    def start(self):
        return range(len(self.string)+1)

    def step(self, state, c):
        new_state = [state[0]+1]
        for i in range(len(state)-1):
            cost = 0 if self.string[i] == c else 1
            new_state.append(min(new_state[i]+1, state[i]+cost, state[i+1]+1))
        return [min(x,self.max_edits+1) for x in new_state]

    def is_match(self, state):
        return state[-1] <= self.max_edits

    def can_match(self, state):
        return min(state) <= self.max_edits

    def transitions(self, state):
        return set(c for (i,c) in enumerate(self.string) if state[i] <= self.max_edits)


def autocomplete_with_levenshtein(root, prefix, max_distance):
    levenshtein_automaton = LevenshteinAutomaton(prefix, max_distance)

    def dfs_with_levenshtein(node, current_word, state_levenshtein, complete_words):
        if node.final and levenshtein_automaton.is_match(state_levenshtein):
            complete_words.append(current_word)

        for next_node, char, _ in node.next:
            if next_node is None or char is None:
                continue

            # Calcula a nova distância de Levenshtein considerando apenas as transições existentes no FST
            new_state_levenshtein = levenshtein_automaton.step(state_levenshtein, char)
            if levenshtein_automaton.can_match(new_state_levenshtein):
                dfs_with_levenshtein(next_node, current_word + char, new_state_levenshtein, complete_words)

    complete_words = []
    initial_state_levenshtein = levenshtein_automaton.start()
    dfs_with_levenshtein(root, "", initial_state_levenshtein, complete_words)
    return complete_words










# class SparseLevenshteinAutomaton:
#     def __init__(self, string, n):
#         self.string = string
#         self.max_edits = n

#     def start(self):
#         return (range(self.max_edits+1), range(self.max_edits+1))

#     def step(self, tuple, c):
#         if tuple[0] and tuple[0][0] == 0 and tuple[1][0] < self.max_edits:
#             new_indices = [0]
#             new_values = [tuple[1][0] + 1]
#         else:
#             new_indices = []
#             new_values = []

#         for j,i in enumerate(tuple[0]):
#             if i == len(self.string): break
#             cost = 0 if self.string[i] == c else 1
#             val = tuple[1][j] + cost
#             if new_indices and new_indices[-1] == i:
#                 val = min(val, new_values[-1] + 1)
#             if j+1 < len(tuple[0]) and tuple[0][j+1] == i+1:
#                 val = min(val, tuple[1][j+1] + 1)
#             if val <= self.max_edits:
#                 new_indices.append(i+1)
#                 new_values.append(val)

#         return (new_indices, new_values)

#     def is_match(self, tuple):
#         return bool(tuple[0]) and tuple[0][-1] == len(self.string)

#     def can_match(self, indices, values):
#         return bool(indices)

#     def transitions(self, indices, values):
#         return set(self.string[i] for i in indices if i < len(self.string))



# # use the automaton to build a DFA

# counter = [0] # list is a hack for mutable lexical scoping
# states = {}
# transitions = []
# matching = []

# lev = SparseLevenshteinAutomaton("plan", 10)

# def explore(state):
#     key = (tuple(state[0]),tuple(state[1])) # lists can't be hashed in Python because they are mutable, so convert to a tuple
#     if key in states: return states[key]
#     i = counter[0]
#     counter[0] += 1
#     states[key] = i
#     if lev.is_match(state): matching.append(i)
#     for c in lev.transitions(state) | set(['*']):
#         newstate = lev.step(state, c)
#         j = explore(newstate)
#         transitions.append((i, j, c))
#     return i

# explore(lev.start())

# transitions.sort(key=lambda tup: tup[0])

# # output to graphviz

# print ("digraph G {")
# for t in transitions:
#     print ('%s -> %s [label=" %s "]' % t)
# for i in matching:
#     print ('%s [style=filled]' % i)
# print ("}")

