import copy
from graphviz import Digraph
from queue import Queue
import curses

class State:
    def __init__(self):
        self.next = []  
        self.output = []
        self.final = False
        
    def hashable_state(self):
      # Cria uma representação hashable do estado
      transitions = tuple((char, id(next_state)) for next_state, char, _ in self.next)
      # Certifique-se de que self.output seja uma lista antes de convertê-lo para tupla
      output_tuple = tuple(self.output) if self.output is not None else tuple()
      return (transitions, output_tuple, self.final)
        
def longest_common_prefix(str1, str2):
    min_length = min(len(str1), len(str2))
    common_prefix = ""

    for i in range(min_length):
        if str1[i] == str2[i]:
            common_prefix += str1[i]
        else:
            break
    return common_prefix

def new_state():
    return State()

def is_final(state):          
    return state.final

def set_final(state,is_final):
  if is_final:
    state.next= [(None, None,"")]
  state.final = is_final

def transition(state, char):
    final_state = None
    for next_state in state.next:
        if next_state[1] == char:
            final_state = state.next[state.next.index(next_state)][0]
        return final_state

def set_transition(from_state, char, to_state):
   for state in from_state.next:
       if state[1] == char:
          from_state.next[from_state.next.index(state)] = (to_state, ) + from_state.next[from_state.next.index(state)][1:]
          return
   from_state.next.append((to_state, char, ''))


def state_output(state):
  return state.output

def set_state_output(state, output):
    state.output = output
    
def output(state, char):
    string =''
    for next_state in state.next:
      if next_state[1] == char:
        string = state.next[state.next.index(next_state)][2]
    return string
  
def set_output(state, char, string):
    for next_state in state.next:
        if next_state[1] == char:
            state.next[state.next.index(next_state)] = state.next[state.next.index(next_state)][:2] + (string, )

def clear_state(state):
    state.next = []
    state.output = []
    state.final = False

def member(state_dict, state):
    # Usa a representação hashable para verificar a presença do estado
    hashable = state.hashable_state()
    return state_dict.get(hashable) 

def print_transducer(file, state):
    for char, to_state in state.next.items():
        file.write("%d %d %s %s\n" % (state, to_state, char, output(state, char)))
        print_transducer(file, to_state)

def FindMinimized(state_dict, state):
    hashable = state.hashable_state()
    if hashable in state_dict:
        return state_dict[hashable]
    else:
        new_state = copy.copy(state)
        state_dict[hashable] = new_state
        return new_state
      
def create_fst(words):
  # CurrentWord = ""
  PreviousWord = ''
  alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
  TempStates = []
  MinimalTransducerStatesDictionary ={}
  # InitialState = None
  # CurrentOutput = ""
  # WordSuffix = ""
  # CommonPrefix = ""
  # TempString = ""
  max_word_size = 0
  
  for word in words:
    if len(word) > max_word_size:
      max_word_size = len(word)

  for i in range(max_word_size + 1):
    TempStates.append(new_state())

  clear_state(TempStates[0])

  a = 1
  for word in words:
    
    CurrentWord = word
    CurrentOutput = str(a)
    a = a + 1
    i = 1
    while (i <= len(CurrentWord)) and (i <= len(PreviousWord)) and (PreviousWord[i-1] == CurrentWord[i-1]):  
      i = i + 1
    
    PrefixLengthPlus1 = i
    
    for i in range(len(PreviousWord), PrefixLengthPlus1 - 1, -1):
      set_transition(TempStates[i-1], PreviousWord[i-1], FindMinimized(MinimalTransducerStatesDictionary,TempStates[i]))

    for i in range(PrefixLengthPlus1, len(CurrentWord) + 1):
      clear_state(TempStates[i])
      set_transition(TempStates[i-1], CurrentWord[i-1], TempStates[i])

    if CurrentWord is not PreviousWord:
      set_final(TempStates[len(CurrentWord)], True)
      set_state_output(TempStates[len(CurrentWord)], [])

    for j in range(1, PrefixLengthPlus1):
      CommonPrefix = longest_common_prefix(output(TempStates[j-1], CurrentWord[j-1]),CurrentOutput)
      WordSuffix = output(TempStates[j-1],CurrentWord[j-1]).replace(CommonPrefix,'')
      set_output(TempStates[j-1],CurrentWord[j-1],CommonPrefix)
      
      for ch in alphabet:
        if transition(TempStates[j],ch) is not None:
          set_output(TempStates[j],ch,WordSuffix+output(TempStates[j],ch))
      
      if is_final(TempStates[j]):
          tempSet = []
          if state_output(TempStates[j]):
              for tempString in state_output(TempStates[j]):
                tempSet.append(WordSuffix + tempString)
          set_state_output(TempStates[j], tempSet)
      
      CurrentOutput = CurrentOutput.replace(CommonPrefix, '')          
    
    if CurrentWord == PreviousWord:
      set_state_output(TempStates[len(CurrentWord)], state_output(TempStates[len(CurrentWord)]).append(CurrentOutput))
    else:
      set_output(TempStates[PrefixLengthPlus1-1], CurrentWord[PrefixLengthPlus1-1], CurrentOutput)

    PreviousWord = CurrentWord

  for i in range(len(CurrentWord), 0, -1):
    set_transition(TempStates[i-1], PreviousWord[i-1], FindMinimized(MinimalTransducerStatesDictionary,TempStates[i]))
  
  InitialState = FindMinimized(MinimalTransducerStatesDictionary,TempStates[0])

  return InitialState, MinimalTransducerStatesDictionary



def autoComplete(fst, prefix):
  def find_state_for_prefix(current_state, suffix):
    for char in suffix:
      next_state = None
      for trans in current_state.next:
        if trans[1] == char:
          next_state=trans[0]
          break
      if next_state is None:
        return None
      current_state = next_state
    return current_state
  
  def dfs(initial_state, prefix, words):
    if initial_state.final:
      words.append(prefix)
    for next_node,char,_ in initial_state.next:
      if char is not None:
        dfs(next_node, prefix+char,words)
        
        
  starting_state = find_state_for_prefix(fst,prefix)
  if starting_state is None:
    return []
  
  words=[]
  dfs(starting_state,prefix,words)
  return words

def read_words_from_file(file_path):
    words = []
    with open(file_path, 'r') as file:
        for word in file:
            words.append(word.strip())
    return words  # Ordena a lista de palavras
  
def count_states(fst):
    visited = set()
    count = 0

    def dfs(state):
        nonlocal count
        if state in visited:
            return
        visited.add(state)
        count += 1
        for next_state, _, _ in state.next:
            if next_state is not None:
                dfs(next_state)

    dfs(fst)
    return count

# palavras= read_words_from_file("dicionario_ordenado.txt")

# teste_graphviz = ['woof','wood','mood','snuff']

# fst,out = create_fst(palavras)

# def main(stdscr):
#     # Inicializa a tela
#     curses.curs_set(1)
#     stdscr.clear()
#     height, width = stdscr.getmaxyx()

#     # Variáveis para armazenar a entrada e as sugestões
#     input_str = ""
#     suggestions = []

#     while True:
#         stdscr.clear()

#         # Mostra a entrada atual
#         stdscr.addstr(0, 0, "Digite: " + input_str[:width-10])

#         # Mostra as sugestões
#         for idx, word in enumerate(suggestions):
#             if idx + 1 < height:
#               stdscr.addstr(idx + 1, 0, word[:width-1])

#         # Captura a próxima tecla pressionada
#         key = stdscr.getch()

#         # Se for Enter, sai do loop
#         if key == curses.KEY_ENTER or key in [10, 13]:
#             break

#         # Se for uma tecla de caractere, adiciona à string de entrada
#         elif key >= 32 and key <= 126:  # Código ASCII para caracteres imprimíveis
#             input_str += chr(key)
#             # Atualiza as sugestões
#             suggestions = autoComplete(fst, input_str)

#         elif key == curses.KEY_BACKSPACE or key == 8:
#           input_str = input_str[:-1]  # Remove o último caractere
#           # Atualiza as sugestões
#           suggestions = autoComplete(fst, input_str)
        
#         # Atualiza a tela
#         stdscr.refresh()
        
# função para desenho do automato
# def fst_to_graphviz(initial_state):
#     dot = Digraph(comment='Finite State Transducer')
#     visited_states = set()  # Conjunto de estados visitados
#     state_queue = Queue()   # Fila para a busca em largura
#     state_ids = {}          # Dicionário para mapear estados para IDs
#     next_id = 0             # Contador para gerar IDs sequenciais

#     # Função auxiliar para adicionar um nó ao gráfico
#     def add_node(state):
#         if state in visited_states:
#             return

#         nonlocal next_id
#         state_id = str(next_id)
#         state_ids[state] = state_id
#         next_id += 1
#         # Verifica se o estado é um estado final (is_end_of_word == True)
#         node_shape = 'doublecircle' if state.final else 'circle'
#         dot.node(state_id, label=state_id, shape=node_shape)
#         visited_states.add(state)
#         state_queue.put(state)

#     add_node(initial_state)  # Inicia a travessia pelo estado inicial

#     while not state_queue.empty():
#         current_state = state_queue.get()
#         current_state_id = state_ids[current_state]

#         for next_state, char, output in current_state.next:
#             if next_state is not None:
#                 if next_state not in visited_states:
#                     add_node(next_state)
#                 next_state_id = state_ids[next_state]
#                 label = f"{char}" if char and output else char or output or 'ε'
#                 dot.edge(current_state_id, next_state_id, label=label)

#     return dot

# estado_incial, _ = create_fst(teste_graphviz)
# dot = fst_to_graphviz(estado_incial)
# dot.render('output',view=True)

# curses.wrapper(main)