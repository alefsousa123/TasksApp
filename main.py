import tkinter as tk
from tkinter import ttk, font, messagebox
from tkinter import PhotoImage
import os
import json

# Caminhos absolutos para os arquivos de imagem (ajuste conforme necessário)
edit_image_path = "C:/Users/lefaz/OneDrive/Documentos/GitHub/TasksApp/edit.png"
delete_image_path = "C:/Users/lefaz/OneDrive/Documentos/GitHub/TasksApp/delete.png"

# Função para carregar imagem com verificação
def carregar_imagem(caminho):
    if os.path.isfile(caminho):
        return PhotoImage(file=caminho).subsample(3, 3)
    else:
        messagebox.showerror("Erro", f"Arquivo de imagem não encontrado: {caminho}")
        return None

# Função para salvar tarefas em um arquivo JSON
def salvar_tarefas(tarefas):
    try:
        with open("tasks.json", "w") as file:
            json.dump(tarefas, file)
        print(f"Tarefas salvas: {tarefas}")
    except Exception as e:
        print(f"Erro ao salvar tarefas: {e}")

# Função para carregar tarefas de um arquivo JSON
def carregar_tarefas():
    try:
        if os.path.isfile("tasks.json"):
            with open("tasks.json", "r") as file:
                return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Erro ao carregar tarefas: {e}")
        messagebox.showerror("Erro", "Arquivo de tarefas corrompido. Iniciando com uma lista de tarefas vazia.")
    return []

# Criando janela
janela = tk.Tk()
janela.title("TasksApp")
janela.configure(bg="#F0F0F0")
janela.geometry("500x600")

# Carregando as imagens e ajustando seu tamanho
icon_editar = carregar_imagem(edit_image_path)
icon_deletar = carregar_imagem(delete_image_path)

# Certifica-se de que as imagens foram carregadas antes de continuar
if icon_editar is None or icon_deletar is None:
    janela.withdraw()
    messagebox.showerror("Erro", "Imagens não foram carregadas corretamente. Verifique os caminhos dos arquivos.")
    janela.destroy()
else:
    frame_em_edicao = None
    tarefa_em_edicao = None
    tarefas = carregar_tarefas()
    print(f"Tarefas carregadas ao iniciar: {tarefas}")

    def add_tarefa():
        global frame_em_edicao, tarefa_em_edicao

        tarefa = entrada_tarefa.get().strip()
        if tarefa and tarefa != "Escreva sua tarefa aqui":
            if frame_em_edicao is not None:
                atualizar_tarefa(tarefa)
                frame_em_edicao = None
                tarefa_em_edicao = None
            else:
                adicionar_item_tarefa(tarefa)
                entrada_tarefa.delete(0, tk.END)
        else:
            messagebox.showwarning("Entrada inválida!", "Por favor, insira uma tarefa.")
        salvar_tarefas(tarefas)

    def adicionar_item_tarefa(tarefa, riscada=False, inicial=False):
        print(f"Adicionando tarefa: {tarefa} - Riscada: {riscada}")
        frame_tarefa = tk.Frame(canvas_interior, bg="white", bd=1, relief=tk.SOLID)

        canvas_text = tk.Canvas(frame_tarefa, bg="white", width=300, height=50)
        canvas_text.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)

        text_id = canvas_text.create_text(10, 25, text=tarefa, font=("Helvetica", 16), anchor="w")

        if riscada:
            canvas_text.itemconfig(text_id, font=("Helvetica", 16, 'overstrike'))

        botao_editar = tk.Button(frame_tarefa, image=icon_editar, command=lambda f=frame_tarefa, c=canvas_text, t=text_id: preparar_edicao(f, c, t), relief=tk.FLAT)
        botao_editar.pack(side=tk.RIGHT, padx=5)

        botao_deletar = tk.Button(frame_tarefa, image=icon_deletar, command=lambda f=frame_tarefa, t=tarefa: deletar_tarefa(f, t), relief=tk.FLAT)
        botao_deletar.pack(side=tk.RIGHT, padx=5)

        checkbutton = ttk.Checkbutton(frame_tarefa, command=lambda c=canvas_text, t=text_id: alternar_riscado(c, t))
        checkbutton.pack(side=tk.RIGHT, padx=5)

        frame_tarefa.pack(fill=tk.X, padx=5, pady=5)

        canvas_interior.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        if not inicial:
            tarefas.append({'tarefa': tarefa, 'riscada': riscada})
            salvar_tarefas(tarefas)

    def preparar_edicao(frame, canvas, text_id):
        global frame_em_edicao, tarefa_em_edicao
        entrada_tarefa.delete(0, tk.END)
        entrada_tarefa.insert(0, canvas.itemcget(text_id, 'text'))
        frame_em_edicao = frame
        tarefa_em_edicao = canvas.itemcget(text_id, 'text')

    def atualizar_tarefa(nova_tarefa):
        global frame_em_edicao, tarefa_em_edicao
        if frame_em_edicao is not None and tarefa_em_edicao is not None:
            for widget in frame_em_edicao.winfo_children():
                if isinstance(widget, tk.Canvas):
                    text_id = widget.find_withtag("all")[0]
                    widget.itemconfig(text_id, text=nova_tarefa)
                    break
            for item in tarefas:
                if item['tarefa'] == tarefa_em_edicao:
                    item['tarefa'] = nova_tarefa
                    break
            frame_em_edicao = None
            tarefa_em_edicao = None
            salvar_tarefas(tarefas)

    def deletar_tarefa(frame, tarefa):
        global tarefas
        print(f"Deletando tarefa: {tarefa}")
        tarefas = [item for item in tarefas if item['tarefa'] != tarefa]
        frame.destroy()
        salvar_tarefas(tarefas)
        print(f"Tarefas restantes após deletar: {tarefas}")

    def alternar_riscado(canvas, text_id):
        current_text = canvas.itemcget(text_id, 'text')
        for item in tarefas:
            if item['tarefa'] == current_text:
                if item['riscada']:
                    canvas.itemconfig(text_id, font=("Helvetica", 16))
                    item['riscada'] = False
                else:
                    canvas.itemconfig(text_id, font=("Helvetica", 16, 'overstrike'))
                    item['riscada'] = True
                break
        salvar_tarefas(tarefas)

    # Definindo cabeçalho
    fonte_cabecalho = font.Font(family="Helvetica", size=24, weight="bold")
    header_label = tk.Label(janela, text="TasksApp", font=fonte_cabecalho, bg="#F0F0F0")
    header_label.pack(pady=20)

    frame = tk.Frame(janela, bg="#F0F0F0")
    frame.pack(pady=10)

    # Barra de entrada e botão
    entrada_tarefa = tk.Entry(frame, font=("Helvetica", 14), relief=tk.FLAT, bg="white", fg="gray", width=30)
    entrada_tarefa.pack(side=tk.LEFT, padx=10)
    botao_add_task = tk.Button(frame, command=add_tarefa, text="Adicionar Tarefa", bg="#4CAF50", fg="white", height=1, width=15, font=("Roboto", 11), relief=tk.FLAT)
    botao_add_task.pack(side=tk.LEFT, padx=10)

    frame_tasks_list = tk.Frame(janela, bg="white")
    frame_tasks_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame_tasks_list, bg="white")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scroll_bar = tk.Scrollbar(frame_tasks_list, orient="vertical", command=canvas.yview)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scroll_bar.set)
    canvas_interior = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=canvas_interior, anchor="nw")
    canvas_interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Carregar tarefas ao iniciar
    for item in tarefas:
        adicionar_item_tarefa(item['tarefa'], item['riscada'], inicial=True)
        print(f"Tarefa carregada: {item['tarefa']} - Riscada: {item['riscada']}")

    janela.mainloop()
