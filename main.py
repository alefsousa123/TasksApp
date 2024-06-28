import tkinter as tk
from tkinter import ttk, font, messagebox
from tkinter import PhotoImage
import os

# Caminhos absolutos para os arquivos de imagem (ajuste conforme necessário)
edit_image_path = "C:/Users/lefaz/OneDrive/Documentos/GitHub/TasksApp/edit.png"
delete_image_path = "C:/Users/lefaz/OneDrive/Documentos/GitHub/TasksApp/delete.png"

# Verifica o diretório de trabalho atual
print("Diretório de trabalho atual:", os.getcwd())

# Verifica se os arquivos de imagem existem
print("Edit image exists:", os.path.isfile(edit_image_path))
print("Delete image exists:", os.path.isfile(delete_image_path))

# Função para carregar imagem com verificação
def carregar_imagem(caminho):
    if os.path.isfile(caminho):
        return PhotoImage(file=caminho).subsample(3, 3)
    else:
        messagebox.showerror("Erro", f"Arquivo de imagem não encontrado: {caminho}")
        return None

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

    def add_tarefa():
        global frame_em_edicao

        tarefa = entrada_tarefa.get().strip()
        if tarefa and tarefa != "Escreva sua tarefa aqui":
            if frame_em_edicao is not None:
                atualizar_tarefa(tarefa)
                frame_em_edicao = None
            else:
                adicionar_item_tarefa(tarefa)
                entrada_tarefa.delete(0, tk.END)
        else:
            messagebox.showwarning("Entrada inválida!", "Por favor, insira uma tarefa.")  

    def adicionar_item_tarefa(tarefa):
        frame_tarefa = tk.Frame(canvas_interior, bg="white", bd=1, relief=tk.SOLID)
        
        label_tarefa = tk.Label(frame_tarefa, text=tarefa, font=("Helvetica", 16), bg="white", width=25, height=2, anchor="w")
        label_tarefa.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)

        botao_editar = tk.Button(frame_tarefa, image=icon_editar, command=lambda f=frame_tarefa, l=label_tarefa: preparar_edicao(f, l), relief=tk.FLAT)
        botao_editar.pack(side=tk.RIGHT, padx=5)

        botao_deletar = tk.Button(frame_tarefa, image=icon_deletar, command=lambda f=frame_tarefa: deletar_tarefa(f), relief=tk.FLAT)
        botao_deletar.pack(side=tk.RIGHT, padx=5)

        checkbutton = ttk.Checkbutton(frame_tarefa, command=lambda label=label_tarefa: alternar_sublinhado(label))
        checkbutton.pack(side=tk.RIGHT, padx=5)

        frame_tarefa.pack(fill=tk.X, padx=5, pady=5)

        canvas_interior.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def preparar_edicao(frame, label):
        global frame_em_edicao
        entrada_tarefa.delete(0, tk.END)
        entrada_tarefa.insert(0, label['text'])
        frame_em_edicao = frame

    def atualizar_tarefa(tarefa):
        global frame_em_edicao
        for widget in frame_em_edicao.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(text=tarefa)
        frame_em_edicao = None

    def deletar_tarefa(frame):
        frame.destroy()

    def alternar_sublinhado(label):
        current_font = label.cget("font")
        if "underline" in current_font:
            new_font = current_font.replace("underline", "")
        else:
            new_font = current_font + " underline"
        label.config(font=new_font)

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

    janela.mainloop()