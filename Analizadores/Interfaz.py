import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Text
from AnalizadorLéxico import *
from AnalizadorSintáctico import *
import webbrowser, os, sys, io

bg_color = "#2E2E2E"
fg_color = "#FFFFFF" 

class Interfaz:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("Analizador")
        self.ventana.config(bg=bg_color)
        self.fuente1 = ("Helvetica", 9)
        self.fuente2 = ("Helvetica", 12)
        self.area_texto = Text(self.ventana, font=self.fuente1)
        self.area_consola = Text(self.ventana, font=self.fuente1)
        self.area_texto.grid(row=0, column=0, padx=10, pady=10)
        self.area_consola.grid(row=0, column=1, padx=10, pady=10)
        self.archivo_analizado = False
        self.ruta = ''
        self.contenido = ''
        self.listaErrores = []
        self.listaTokens = []
        self.tree = None

    def ventana_principal(self):
        self.ventana.title('BizData')
        self.centrar_ventana()
        self.ventana.resizable(False, False)
        self.componentes()
        self.ventana.mainloop()

    def centrar_ventana(self):
        w, h = 1500, 750
        w_pantalla = self.ventana.winfo_screenwidth()
        h_pantalla = self.ventana.winfo_screenheight()
        x = ((w_pantalla / 2) - (w / 2))
        y = ((h_pantalla / 2) - (h / 2)) - 50
        self.ventana.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

    def componentes(self):
        self.botones()
        self.editor()
        self.consola()

    def botones(self):

        cargar = Button(self.ventana, text='Cargar', width=10, height=2, bg="#474747", fg=fg_color, font=self.fuente2, command=self.botónCargar)
        cargar.place(x=35, y=20)

        analizar = Button(self.ventana, text='Analizar', width=10, height=2, bg="#474747", fg=fg_color, font=self.fuente2, command=self.botónAnalizar)
        analizar.place(x=140, y=20)

        token = Button(self.ventana, text='Reporte de tokens', width=15, height=2, bg="#474747", fg=fg_color, font=self.fuente2, command=self.reporte_tokens)
        token.place(x=1025, y=20)

        error = Button(self.ventana, text='Reporte de errores', width=15, height=2, bg="#474747", fg=fg_color, font=self.fuente2, command=self.reporte_errores)
        error.place(x=1175, y=20)

        grafica = Button(self.ventana, text='Arbol de derivación', width=15, height=2, bg="#474747", fg=fg_color, font=self.fuente2, command=self.grafica)
        grafica.place(x=1325, y=20)

    def editor(self):
        self.area_texto.configure(width=100, height=43)
        self.area_texto.place(x=35, y=80)

    def consola(self):
        self.area_consola.configure(bg='black', fg='white', width=100, height=43)
        self.area_consola.place(x=765, y=80)

    def botónCargar(self): 
        tipos_archivos = [("Archivos .bizdata", "*.bizdata"), ("Todos los archivos", "*.*")]
        archivo = filedialog.askopenfilename(filetypes=tipos_archivos)

        if archivo:
            self.ruta = archivo
            self.area_texto.delete("1.0", "end")
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    self.area_texto.insert("1.0", contenido)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")

    def botónAnalizar(self): 
        try:
            texto = self.area_texto.get("1.0", "end")
            scanner = Léxico()
            listas = scanner.analyzer(texto)

            parser = Sintáctico(listas[0], listas[1])
            scanner.printTokens()
            consola = parser.analyze()
            messagebox.showinfo("Archivo analizado", "Se ha analizado el archivo correctamente.")
            self.area_consola.insert(tk.END, consola[0])
            self.listaErrores = consola[1]
            self.tree = consola[2]
            self.area_consola.configure(state="disabled")
        except:
            messagebox.showerror("Error", "No se pudo analizar el archivo.")

    def reporte_errores(self):
        pass

    def reporte_tokens(self):
        pass

    def grafica(self):
        pass

app = Interfaz()
app.ventana_principal()
