import Fst
import tkinter as tk
from tkinter import scrolledtext
import time
import tracemalloc
import levenshtein

def read_words_from_file(file_path):
    words = []
    with open(file_path, 'r') as file:
        for word in file:
            words.append(word.strip())
    return words  # Ordena a lista de palavras


def update_results():
    prefix = prefix_entry.get()

    # Iniciar o rastreamento de memória
    tracemalloc.start()

    # Medir o tempo e a memória para o FST
    start_time = time.time()
    fst_results = Fst.autoComplete(my_fst, prefix)
    fst_time = time.time() - start_time
    _, fst_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Atualizar as áreas de texto
    fst_text.delete('1.0', tk.END)
    fst_text.insert(tk.END, '\n'.join(fst_results))


    # Atualizar os rótulos de tempo e memória para o FST
    fst_time_label.config(text=f"Tempo do FST: {fst_time:.6f} seg")
    fst_memory_label.config(text=f"Memória do FST: {fst_memory} bytes")

    # Obter a distância de Levenshtein
    try:
        levenshtein_distance = int(levenshtein_entry.get())
    except ValueError:
        levenshtein_distance = 0  # Ou trate o erro conforme necessário

    # Medir o tempo e a memória para o FST com Levenshtein
    tracemalloc.start()
    start_time = time.time()
    fst_levenshtein_results = levenshtein.autocomplete_with_levenshtein(my_fst, prefix, levenshtein_distance)
    fst_levenshtein_time = time.time() - start_time
    _, fst_levenshtein_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Atualizar a área de texto para resultados do FST com Levenshtein
    fst_levenshtein_text.delete('1.0', tk.END)
    fst_levenshtein_text.insert(tk.END, '\n'.join(fst_levenshtein_results))
    
    # Atualizar os rótulos de tempo e memória para o FST com levenshtein
    fst_levenshtein_time_label.config(text=f"Tempo do FST com levenshtein: {fst_levenshtein_time:.6f} seg")
    fst_levenshtein_memory_label.config(text=f"Memória do FST: {fst_levenshtein_memory} bytes")

window = tk.Tk()
window.title("Autocompletar com FST")

# Pegando as palavras
file_path = 'dicionario_ordenado.txt'
words = read_words_from_file(file_path)

# Criando a fst
my_fst, _ = Fst.create_fst(words)
number_of_states = Fst.count_states(my_fst)
print(number_of_states)
# Campo de entrada para o prefixo
prefix_label = tk.Label(window, text="Digite o prefixo:")
prefix_label.pack()
prefix_entry = tk.Entry(window)
prefix_entry.pack()

# Adicionar uma entrada para a distância de Levenshtein
levenshtein_label = tk.Label(window, text="Distância de Levenshtein:")
levenshtein_label.pack()
levenshtein_entry = tk.Entry(window)
levenshtein_entry.pack()

# Área de texto para resultados do FST
fst_label = tk.Label(window, text="Resultados do FST:")
fst_label.pack()
fst_text = scrolledtext.ScrolledText(window, height=10)
fst_text.pack()


# Área de texto para resultados do FST com Levenshtein
fst_levenshtein_label = tk.Label(window, text="Resultados do FST com Levenshtein:")
fst_levenshtein_label.pack()
fst_levenshtein_text = scrolledtext.ScrolledText(window, height=10)
fst_levenshtein_text.pack()

# Rótulos para exibir o tempo e a memória do FST
fst_time_label = tk.Label(window, text="Tempo do FST:")
fst_time_label.pack()
fst_memory_label = tk.Label(window, text="Memória do FST:")
fst_memory_label.pack()

# Rótulos para exibir o tempo e a memória do FST com levenshtein
fst_levenshtein_time_label = tk.Label(window, text="Tempo do FST com levenshtein:")
fst_levenshtein_time_label.pack()
fst_levenshtein_memory_label = tk.Label(window, text="Memória do FST com levenshtein:")
fst_levenshtein_memory_label.pack()

# fst_time_creation_label = tk.Label(window)
# fst_time_creation_label.pack()
# fst_time_creation_label.config(text=f"Tempo para criação da estrutura FST: {fst_time_creation:.6f} seg")

# fst_memory_creation_label = tk.Label(window)
# fst_memory_creation_label.pack()
# fst_memory_creation_label.config(text=f"Memória na criação da estrutura FST: {fst_memory_creation/1000} kB")

prefix_entry.bind('<KeyRelease>', lambda event: update_results())
window.mainloop()
