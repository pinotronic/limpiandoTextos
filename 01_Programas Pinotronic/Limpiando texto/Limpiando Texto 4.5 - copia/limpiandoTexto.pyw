import sys
import tkinter as tk
from tkinter import ttk, StringVar, END, NORMAL
import pyperclip as clipboard
from ManejoArchivos import ManejoArchivo
from Proceso import Operativo

def vp_start_gui():
    global root
    root = tk.Tk()
    app = FRMLimpiandoTexto(root)
    root.mainloop()

class FRMLimpiandoTexto:
    def __init__(self, top=None):
        self.top = top
        self.top.title("Limpiando Texto 4.5")
        self.top.configure(background="#004040")
        self.top.geometry("1365x697")

        self.textoParaModificar = StringVar()
        self.textoqueSustituira = StringVar()
        self.DirectorioArchivo = StringVar()

        self.style = ttk.Style()
        self.style.theme_use('winnative')

        self.Label1 = tk.Label(self.top, text="Limpiando Texto 4.5", font=("Arial",36,"bold"), fg="#f9ff00", bg="#004040")
        self.Label1.place(relx=0.272, rely=0.014, height=39, width=474)

        self.txtCajaTexto = tk.Text(self.top, background="#000000", foreground="#00ff00", wrap="word")
        self.txtCajaTexto.place(relx=0.007, rely=0.086, relheight=0.78, relwidth=0.979)

        self.txbTextoAModificar = tk.Entry(self.top, textvariable=self.textoParaModificar)
        self.txbTextoAModificar.place(relx=0.007, rely=0.89, height=20, relwidth=0.391)

        self.txbTextoModificado = tk.Entry(self.top, textvariable=self.textoqueSustituira)
        self.txbTextoModificado.place(relx=0.41, rely=0.89, height=20, relwidth=0.391)

        self.txbDireccionArchivo = tk.Entry(self.top, textvariable=self.DirectorioArchivo)
        self.txbDireccionArchivo.place(relx=0.007, rely=0.947, height=20, relwidth=0.867)

        self.btnCambiar = tk.Button(self.top, text="+", font=("Segoe UI",18), command=self.envioSustituciondeTexto)
        self.btnCambiar.place(relx=0.85, rely=0.875, height=34, width=47)

        self.btnProceso = tk.Button(self.top, text="🚀", font=("Segoe UI",18), command=self.realizarProceso)
        self.btnProceso.place(relx=0.813, rely=0.875, height=34, width=47)

        self.btnCopiar = tk.Button(self.top, text="📑", font=("Segoe UI",18), command=self.copiarTexto)
        self.btnCopiar.place(relx=0.918, rely=0.875, height=34, width=47)

        self.btnBorrar = tk.Button(self.top, text="🗑", font=("Segoe UI",18), command=self.borrarTexto)
        self.btnBorrar.place(relx=0.954, rely=0.875, height=34, width=47)

        self.btnLeer = tk.Button(self.top, text="🔊", font=("Segoe UI",18), command=self.leerTexto)
        self.btnLeer.place(relx=0.881, rely=0.875, height=34, width=47)

        self.btnAbrir = tk.Button(self.top, text="📁", font=("Segoe UI",18), command=self.cargarTexton)
        self.btnAbrir.place(relx=0.881, rely=0.933, height=34, width=47)

        self.btnGuardar = tk.Button(self.top, text="💾", font=("Segoe UI",18), command=self.guardando)
        self.btnGuardar.place(relx=0.918, rely=0.933, height=34, width=47)

        self.btnSalir = tk.Button(self.top, text="🔒", font=("Segoe UI",18), command=self.salir)
        self.btnSalir.place(relx=0.954, rely=0.933, height=34, width=47)

        self.Operativo = Operativo()

    def cargarTexton(self):
        self.txtCajaTexto.delete(1.0, END)
        textoRecibido, directorio = ManejoArchivo().cargarInformacion()
        self.txtCajaTexto.insert("1.0",textoRecibido)
        self.DirectorioArchivo.set(directorio)

    def borrarTexto(self):
        self.txtCajaTexto.delete(1.0, END)

    def envioSustituciondeTexto(self):
        textoOriginal = self.txtCajaTexto.get(1.0,END)
        texto1 = self.txbTextoAModificar.get()
        texto2 = self.txbTextoModificado.get()
        TextoRecibido = self.Operativo.sustitucionTexto(textoOriginal,texto1,texto2)
        self.txtCajaTexto.config(state=NORMAL)
        self.txtCajaTexto.delete(1.0,END)
        self.txtCajaTexto.insert(END,TextoRecibido)
        self.textoParaModificar.set("")
        self.textoqueSustituira.set("")

    def copiarTexto(self):
        textoOriginal=self.txtCajaTexto.get(1.0, END)
        clipboard.copy(textoOriginal)

    def realizarProceso(self):
        textoOriginal = self.txtCajaTexto.get(1.0, END)
        TextoRecibido = self.Operativo.realizandoProceso(textoOriginal)
        self.txtCajaTexto.config(state=NORMAL)
        self.txtCajaTexto.delete(1.0, END)
        self.txtCajaTexto.insert(END, TextoRecibido)

    def guardando(self):
        textoOriginal = self.txtCajaTexto.get(1.0, END)
        ManejoArchivo.guardarEnArchivo(textoOriginal)

    def leerTexto(self):
        textoOriginal = self.txtCajaTexto.get(1.0, END)
        self.Operativo.leerArchivo(textoOriginal)

    def salir(self):
        sys.exit(0)

if __name__ == '__main__':
    vp_start_gui()
