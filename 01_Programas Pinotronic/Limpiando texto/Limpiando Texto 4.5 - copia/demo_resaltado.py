"""
Demo del Sistema de Resaltado de Palabras
Prueba el resaltado visual durante la lectura TTS
"""

import tkinter as tk
from tkinter import END
import sys
import os

# Agregar path para importar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Proceso import Operativo

class DemoResaltado:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Demo - Resaltado de Palabras TTS")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        # Título
        titulo = tk.Label(
            self.root,
            text="🎨 Demo del Sistema de Resaltado",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        titulo.pack(pady=20)
        
        # Instrucciones
        instrucciones = tk.Label(
            self.root,
            text="Las palabras se resaltarán en AMARILLO mientras se leen.\n"
                 "Observa cómo el resaltado sigue la lectura en tiempo real.",
            font=("Arial", 12),
            bg="#2c3e50",
            fg="#bdc3c7",
            justify="center"
        )
        instrucciones.pack(pady=10)
        
        # Área de texto
        frame_texto = tk.Frame(self.root, bg="#34495e")
        frame_texto.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.texto = tk.Text(
            frame_texto,
            font=("Arial", 12),
            bg="#ecf0f1",
            fg="#2c3e50",
            wrap="word",
            padx=15,
            pady=15
        )
        self.texto.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame_texto, command=self.texto.yview)
        scrollbar.pack(side="right", fill="y")
        self.texto.config(yscrollcommand=scrollbar.set)
        
        # Texto de ejemplo
        texto_ejemplo = """Bienvenido al sistema de resaltado de palabras en tiempo real.

Este es un ejemplo de cómo funciona el resaltado visual durante la lectura.

Cada palabra se iluminará con un fondo amarillo brillante mientras el sistema la pronuncia.

El resaltado te ayuda a seguir la lectura visualmente, mejorando la comprensión del texto.

Esta característica es especialmente útil para:
• Seguimiento visual de la lectura
• Personas con dislexia o dificultades de lectura
• Aprendizaje de nuevos idiomas
• Revisión de textos largos
• Presentaciones y prácticas de oratoria

El sistema se sincroniza automáticamente con la velocidad de la voz.

¡Disfruta de esta nueva característica!"""

        self.texto.insert("1.0", texto_ejemplo)
        
        # Frame de botones
        frame_botones = tk.Frame(self.root, bg="#2c3e50")
        frame_botones.pack(pady=20)
        
        # Botón de Leer
        self.btn_leer = tk.Button(
            frame_botones,
            text="🔊 Leer con Resaltado",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=10,
            command=self.leer_texto,
            cursor="hand2"
        )
        self.btn_leer.pack(side="left", padx=10)
        
        # Botón de Detener
        self.btn_detener = tk.Button(
            frame_botones,
            text="⏹ Detener",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10,
            command=self.detener_lectura,
            state="disabled",
            cursor="hand2"
        )
        self.btn_detener.pack(side="left", padx=10)
        
        # Botón de Limpiar
        btn_limpiar = tk.Button(
            frame_botones,
            text="🗑 Limpiar",
            font=("Arial", 14, "bold"),
            bg="#95a5a6",
            fg="white",
            padx=20,
            pady=10,
            command=self.limpiar_texto,
            cursor="hand2"
        )
        btn_limpiar.pack(side="left", padx=10)
        
        # Estado
        self.label_estado = tk.Label(
            self.root,
            text="Presiona '🔊 Leer con Resaltado' para comenzar",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#3498db"
        )
        self.label_estado.pack(pady=10)
        
        # Inicializar sistema operativo
        self.operativo = Operativo()
        self.operativo.set_texto_widget(self.texto)
        
    def leer_texto(self):
        """Inicia la lectura con resaltado"""
        texto_contenido = self.texto.get("1.0", END)
        
        if not texto_contenido.strip():
            self.label_estado.config(
                text="⚠️ No hay texto para leer",
                fg="#e74c3c"
            )
            return
        
        self.btn_leer.config(state="disabled")
        self.btn_detener.config(state="normal")
        self.label_estado.config(
            text="🔊 Leyendo con resaltado... Observa las palabras en amarillo",
            fg="#f39c12"
        )
        
        # Leer en thread separado
        import threading
        def leer_thread():
            try:
                self.operativo.leerArchivo(texto_contenido)
            finally:
                self.root.after(0, self.finalizar_lectura)
        
        thread = threading.Thread(target=leer_thread, daemon=True)
        thread.start()
    
    def detener_lectura(self):
        """Detiene la lectura actual"""
        self.operativo.detener_lectura()
        self.label_estado.config(
            text="⏹ Lectura detenida",
            fg="#e74c3c"
        )
        self.finalizar_lectura()
    
    def finalizar_lectura(self):
        """Restaura la interfaz después de la lectura"""
        self.btn_leer.config(state="normal")
        self.btn_detener.config(state="disabled")
        self.label_estado.config(
            text="✅ Lectura completada. ¿Viste el resaltado?",
            fg="#27ae60"
        )
    
    def limpiar_texto(self):
        """Limpia el área de texto"""
        self.texto.delete("1.0", END)
        self.label_estado.config(
            text="Escribe o pega texto para probar el resaltado",
            fg="#3498db"
        )
    
    def ejecutar(self):
        """Inicia la aplicación"""
        print("=" * 60)
        print("  DEMO - SISTEMA DE RESALTADO DE PALABRAS")
        print("=" * 60)
        print()
        print("Instrucciones:")
        print("1. Observa el texto de ejemplo en la ventana")
        print("2. Presiona '🔊 Leer con Resaltado'")
        print("3. Observa cómo cada palabra se resalta en AMARILLO")
        print("4. El resaltado se sincroniza con la voz")
        print()
        print("Características:")
        print("✅ Resaltado en tiempo real")
        print("✅ Scroll automático")
        print("✅ Sincronización con voz")
        print("✅ Botón de detener")
        print()
        print("Motor TTS detectado:")
        
        estado = self.operativo.estado_ia()
        if self.operativo.piper_path and self.operativo.piper_model:
            print("🎙️ Piper TTS disponible (sin resaltado)")
        print("🎙️ pyttsx3 disponible (CON RESALTADO) ✅")
        if estado.get('disponible'):
            print("🎙️ gTTS disponible (sin resaltado)")
        
        print()
        print("⚠️ IMPORTANTE:")
        print("   El resaltado SOLO funciona con pyttsx3")
        print("   (El programa usará pyttsx3 automáticamente)")
        print()
        print("=" * 60)
        
        self.root.mainloop()

if __name__ == "__main__":
    try:
        demo = DemoResaltado()
        demo.ejecutar()
    except Exception as e:
        print(f"Error al ejecutar demo: {e}")
        import traceback
        traceback.print_exc()
