import tkinter as Tk
from tkinter.constants import COMMAND, DISABLED
from tkinter import messagebox

import tkinter.ttk as Ttk


from ply import *

ventana = Tk.Tk()
ventana.geometry("600x400")
ventana.title("JPR | OCL 1 | VJ2021")
ventana.resizable(0,0)



bar_menu=Tk.Menu(ventana)
ventana.config(menu=bar_menu)

bm_Archivo=Tk.Menu(bar_menu,tearoff=0)
bm_Archivo.add_command(label="Abrir")
bm_Archivo.add_command(label="Nuevo")
bm_Archivo.add_command(label="Guardar")
bm_Archivo.add_command(label="Guardar Como")
bm_Archivo.add_separator()
bm_Archivo.add_command(label="Salir...",command=ventana.destroy)

bm_Herramientas=Tk.Menu(bar_menu,tearoff=0)
bm_Herramientas.add_command(label="Interpretar")
bm_Herramientas.add_command(label="Debugger")

bm_Reportes=Tk.Menu(bar_menu,tearoff=0)
bm_Reportes.add_command(label="Reporte de Errores")
bm_Reportes.add_command(label="Generar Arbol AST")
bm_Reportes.add_command(label="Reporte de Tabla de Simbolos")



bm_AcercaDe=Tk.Menu(bar_menu,tearoff=0)
bm_AcercaDe.add_command(label="Autor", command=lambda:[messagebox.showinfo("JPR - OCL1","Carlos Emilio Campos Moran \n201612332")])




bar_menu.add_cascade(label="Archivo",menu=bm_Archivo)
bar_menu.add_cascade(label="Herramientas",menu=bm_Herramientas)
bar_menu.add_cascade(label="Reportes",menu=bm_Reportes)
bar_menu.add_cascade(label="Acerca De",menu=bm_AcercaDe)

ventana.mainloop()