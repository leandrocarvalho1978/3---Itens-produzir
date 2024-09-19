import os
import tkinter as tk
from tkinter import ttk
import subprocess
import json

# Caminho para o arquivo Pedidos Pagos
pedidos_pagos_path = r'C:\Users\leand\OneDrive\Desktop\Aplicativos\Pedidos Pagos.txt'

# Diretório onde as pastas estão localizadas
base_dir = r'C:\Users\leand\3D Objects'

# Caminho para o arquivo JSON que salvará o estado dos itens produzidos
json_path = r'C:\Users\leand\OneDrive\Desktop\Aplicativos\3 - Itens à produzir.json'

def aplicar_tema(root):
    """Aplica um tema estilizado à interface."""
    style = ttk.Style(root)
    style.theme_use("clam")  # Utilizando o tema 'clam' do ttk
    
    # Personalizando botões e listboxes
    style.configure("TButton", font=("Arial", 12), background="#4CAF50", foreground="white")
    style.configure("TLabel", font=("Arial", 12, "bold"), foreground="#333333")
    style.configure("TFrame", background="#E0E0E0")
    style.configure("TScrollbar", troughcolor="#BDBDBD", bordercolor="#333333", background="#888888")
    
    # Configuração da Listbox personalizada
    root.option_add("*Listbox*Background", "#F5F5F5")
    root.option_add("*Listbox*Foreground", "#333333")
    root.option_add("*Listbox*Font", "Arial 10")

def abrir_pasta(caminho):
    subprocess.Popen(f'explorer "{caminho}"')

def listar_itens_pasta(pasta):
    caminho_completo = os.path.join(base_dir, pasta)
    itens = []
    for item in os.listdir(caminho_completo):
        item_path = os.path.join(caminho_completo, item)
        if os.path.isdir(item_path) or os.path.splitext(item_path)[1].lower() == '.lnk':
            itens.append(item)
    return itens

def on_double_click(event, pasta, item):
    item_path = os.path.join(base_dir, pasta, item)
    abrir_pasta(item_path)

def alterar_cor_texto(listbox, estados, pasta):
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        item = listbox.get(index)
        item_key = f"{pasta}_{item}"
        current_color = listbox.itemcget(index, "fg")
        if current_color == "gray":
            listbox.itemconfig(index, {'fg': 'black'})
            estados[item_key] = False
        else:
            listbox.itemconfig(index, {'fg': 'gray'})
            estados[item_key] = True
        salvar_estados(estados)

def criar_listbox(root, pasta, row, col, estados):
    frame = ttk.Frame(root)
    frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    label = ttk.Label(frame, text=pasta)
    label.pack()

    itens = listar_itens_pasta(pasta)
    
    listbox = tk.Listbox(frame, height=40)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    for idx, item in enumerate(itens):
        listbox.insert(tk.END, item)
        item_key = f"{pasta}_{item}"
        if estados.get(item_key, False):
            listbox.itemconfig(idx, {'fg': 'gray'})

    listbox.bind("<Double-1>", lambda event, p=pasta: on_double_click(event, p, listbox.get(tk.ACTIVE)))

    return listbox

def carregar_estados():
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_estados(estados):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(estados, f, ensure_ascii=False, indent=4)

def criar_botao_alterar_cor(root, listboxes, estados):
    def on_click():
        for listbox, pasta in listboxes:
            alterar_cor_texto(listbox, estados, pasta)
    
    botao = ttk.Button(root, text="Marcar como Produzido", command=on_click)
    botao.grid(row=linhas, column=0, columnspan=colunas, padx=10, pady=10, sticky="nsew")

def refresh(root, listboxes, estados):
    with open(pedidos_pagos_path, 'r', encoding='utf-8') as f:
        pastas_pagas = f.read().splitlines()

    for listbox, _ in listboxes:
        listbox.destroy()

    listboxes.clear()
    for i, pasta in enumerate(pastas_pagas):
        row = i // colunas
        col = i % colunas
        listbox = criar_listbox(root, pasta, row, col, estados)
        listboxes.append((listbox, pasta))

def criar_botao_refresh(root, listboxes, estados):
    def on_click():
        refresh(root, listboxes, estados)
    
    botao = ttk.Button(root, text="Refresh", command=on_click)
    botao.grid(row=linhas + 1, column=0, columnspan=colunas, padx=10, pady=10, sticky="nsew")

def main():
    global colunas, linhas

    with open(pedidos_pagos_path, 'r', encoding='utf-8') as f:
        pastas_pagas = f.read().splitlines()

    root = tk.Tk()
    root.title("Itens à Produzir")

    aplicar_tema(root)  # Aplicar tema personalizado

    colunas = 3
    linhas = (len(pastas_pagas) + colunas - 1) // colunas

    estados = carregar_estados()
    listboxes = []

    for i, pasta in enumerate(pastas_pagas):
        row = i // colunas
        col = i % colunas
        listbox = criar_listbox(root, pasta, row, col, estados)
        listboxes.append((listbox, pasta))

    for i in range(colunas):
        root.grid_columnconfigure(i, weight=1)
    for i in range(linhas):
        root.grid_rowconfigure(i, weight=1)

    criar_botao_alterar_cor(root, listboxes, estados)
    criar_botao_refresh(root, listboxes, estados)

    root.mainloop()

if __name__ == "__main__":
    main()
