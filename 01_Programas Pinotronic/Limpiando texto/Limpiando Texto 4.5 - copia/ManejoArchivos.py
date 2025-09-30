import sys
from tkinter import filedialog, messagebox

class ManejoArchivo:
    def __init__(self):
        pass
    def cargarInformacion(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, 'r', encoding="utf-8") as file:
                buff = file.read()
            return buff,filename
        return "", ""
    @staticmethod
    def guardarEnArchivo(Archivoagurdar):
        nombrearch = filedialog.asksaveasfilename(initialdir="/", title="Guardar como", filetypes=(("txt files","*.txt"),("todos los archivos","*.*")))
        if nombrearch!='':
            with open(nombrearch, "w", encoding="utf-8") as archi1:
                archi1.write(Archivoagurdar)
            messagebox.showinfo("Información", "Los datos fueron guardados en el archivo.")
