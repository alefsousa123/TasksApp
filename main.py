import tkinter as tk
from tkinter import ttk, font, messagebox
from tkinter import messagebox

#criando janela
janela = tk.Tk()
janela.title("TasksApp")
janela.configure(bg= "#F0F0F0")
janela.geometry("500x600")

#Definindo cabeçalho
fonte_cabecalho = font.Font(family="Helvetica", size=24, weight="bold")
header_label = tk.Label(janela, text="TasksApp", font=fonte_cabecalho, bg="#F0F0F0")
header_label.pack(pady=20)

frame = tk.Frame(janela, bg="#F0F0F0")
frame.pack(pady=10)

#barra e botão
entrada_tarefa = tk.Entry(frame, font=("Helvetica", 14), relief=tk.FLAT, bg="white", fg="gray", width= 30)
entrada_tarefa.pack(side=tk.LEFT, padx=10)
botao_add_task = tk.Button(frame, text="adicionar tarefa", bg="#4CAF50", fg= "white", height=1, width=15, font=("roboto", 11), relief=tk.FLAT)
botao_add_task.pack(side=tk.LEFT, padx=10)

frame_tasks_list = tk.Frame(janela, bg="white")
frame_tasks_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas= tk.Canvas(frame_tasks_list, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


janela.mainloop()