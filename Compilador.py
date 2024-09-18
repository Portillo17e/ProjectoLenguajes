import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import re

# Definición de los tokens válidos
tokens_reservados = {
    'palabras_reservadas': ['entero', 'decimal', 'booleano', 'cadena', 'si', 'sino', 'mientras', 'hacer', 'verdadero', 'falso'],
    'operadores': ['+', '-', '*', '/', '%', '=', '==', '<', '>', '>=', '<='],
    'signos': ['(', ')', '{', '}', '“', ';'],
    'numeros': r'\d+',
    'identificadores': r'[a-zA-Z_][a-zA-Z0-9_]*'
}

# Función para cargar el archivo de texto
def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if archivo:
        with open(archivo, 'r') as f:
            contenido = f.read()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, contenido)
        analizar_texto(contenido)

# Función para analizar el contenido del archivo
def analizar_texto(contenido):
    lineas = contenido.splitlines()
    tokens_encontrados = []
    errores_lexicos = []
    
    for numero_linea, linea in enumerate(lineas, 1):
        tokens, errores = analizar_linea(linea, numero_linea)
        tokens_encontrados.extend(tokens)
        errores_lexicos.extend(errores)
    
    mostrar_resultados(tokens_encontrados, errores_lexicos)

# Función para analizar cada línea de texto
def analizar_linea(linea, numero_linea):
    tokens_encontrados = []
    errores_lexicos = []
    
    palabras = linea.split()
    for palabra in palabras:
        if palabra in tokens_reservados['palabras_reservadas']:
            tokens_encontrados.append((palabra, 'Palabra Reservada', numero_linea))
        elif palabra in tokens_reservados['operadores']:
            tokens_encontrados.append((palabra, 'Operador', numero_linea))
        elif palabra in tokens_reservados['signos']:
            tokens_encontrados.append((palabra, 'Signo', numero_linea))
        elif re.match(tokens_reservados['numeros'], palabra):
            tokens_encontrados.append((palabra, 'Número', numero_linea))
        elif re.match(tokens_reservados['identificadores'], palabra):
            tokens_encontrados.append((palabra, 'Identificador', numero_linea))
        else:
            errores_lexicos.append((palabra, 'Error Léxico', numero_linea))
    
    return tokens_encontrados, errores_lexicos

# Función para mostrar los tokens y errores encontrados en la interfaz gráfica
def mostrar_resultados(tokens, errores):
    resultados_texto.delete(1.0, tk.END)
    
    if errores:
        resultados_texto.insert(tk.END, "⚠️ Errores Léxicos encontrados:\n", "error")
        for error in errores:
            resultados_texto.insert(tk.END, f"{error[0]} en la línea {error[2]} ({error[1]})\n", "error")
    
    if tokens:
        resultados_texto.insert(tk.END, "\n✔️ Tokens encontrados:\n", "token")
        for token in tokens:
            resultados_texto.insert(tk.END, f"Token: {token[0]} - Tipo: {token[1]} - Línea: {token[2]}\n", "token")

# Configuración de la interfaz gráfica mejorada
root = tk.Tk()
root.title("🔍 Analizador Léxico - Proyecto 1")
root.geometry("750x550")
root.configure(bg='#2c3e50')

# Estilo mejorado
style = ttk.Style(root)
style.configure('TButton', font=('Arial', 12), padding=10, relief="flat", background="#34495e", foreground="#ecf0f1")
style.configure('TLabel', font=('Arial', 11, 'bold'), background='#2c3e50', foreground='#ecf0f1')

# Crear un frame superior para organización
frame_superior = ttk.Frame(root, style="TFrame", padding="10 10 10 10")
frame_superior.pack(pady=15)

# Etiqueta descriptiva
etiqueta = ttk.Label(frame_superior, text="📄 Cargar archivo de texto para análisis léxico:", style="TLabel")
etiqueta.pack(side=tk.LEFT, padx=5)

# Botón para cargar archivo con icono y estilo
btn_cargar = ttk.Button(frame_superior, text="Cargar Archivo", command=cargar_archivo)
btn_cargar.pack(side=tk.LEFT)

# Separador visual
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x', padx=20, pady=10)

# Área de texto para mostrar el contenido del archivo cargado
label_text_area = ttk.Label(root, text="📑 Contenido del Archivo:", style="TLabel")
label_text_area.pack(pady=5)
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=85, height=10, font=('Courier', 11), bg="#34495e", fg="#ecf0f1")
text_area.pack(padx=20, pady=10)

# Separador visual
separator2 = ttk.Separator(root, orient='horizontal')
separator2.pack(fill='x', padx=20, pady=10)

# Área de texto para mostrar los resultados del análisis
label_resultados = ttk.Label(root, text="📊 Resultados del Análisis Léxico:", style="TLabel")
label_resultados.pack(pady=5)
resultados_texto = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=85, height=10, font=('Courier', 11), bg="#34495e", fg="#ecf0f1")
resultados_texto.tag_configure("error", foreground="red", font=('Courier', 11, 'bold'))
resultados_texto.tag_configure("token", foreground="lightgreen", font=('Courier', 11, 'bold'))
resultados_texto.pack(padx=20, pady=10)

# Ejecutar la interfaz gráfica
root.mainloop()
