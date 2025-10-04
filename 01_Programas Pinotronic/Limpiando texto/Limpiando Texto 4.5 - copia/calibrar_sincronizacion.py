"""
Script de Calibración de Sincronización
Ayuda a ajustar el resaltado para que vaya perfectamente sincronizado con la voz
"""

import tkinter as tk
from tkinter import ttk, END
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Proceso import Operativo

class CalibradorSincronizacion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔧 Calibrador de Sincronización TTS")
        self.root.geometry("900x700")
        self.root.configure(bg="#34495e")
        
        # Variables de configuración
        self.delay_inicial = tk.DoubleVar(value=0.15)
        self.factor_longitud = tk.DoubleVar(value=0.02)
        
        self.crear_interfaz()
        
        # Operativo
        self.operativo = None
        
    def crear_interfaz(self):
        # Título
        titulo = tk.Label(
            self.root,
            text="🔧 Calibrador de Sincronización",
            font=("Arial", 22, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        )
        titulo.pack(pady=15)
        
        # Subtítulo
        subtitulo = tk.Label(
            self.root,
            text="Ajusta la sincronización del resaltado para que coincida perfectamente con la voz",
            font=("Arial", 11),
            bg="#34495e",
            fg="#bdc3c7"
        )
        subtitulo.pack(pady=5)
        
        # Frame de configuración
        frame_config = tk.LabelFrame(
            self.root,
            text="⚙️ Configuración de Sincronización",
            font=("Arial", 12, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
            padx=20,
            pady=15
        )
        frame_config.pack(pady=15, padx=20, fill="x")
        
        # Delay Inicial
        tk.Label(
            frame_config,
            text="⏱️ Delay Inicial (segundos):",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#ecf0f1"
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        delay_frame = tk.Frame(frame_config, bg="#2c3e50")
        delay_frame.grid(row=0, column=1, sticky="ew", padx=10)
        
        self.delay_scale = tk.Scale(
            delay_frame,
            from_=0.0,
            to=0.5,
            resolution=0.05,
            orient="horizontal",
            variable=self.delay_inicial,
            bg="#34495e",
            fg="#ecf0f1",
            highlightthickness=0,
            length=250
        )
        self.delay_scale.pack(side="left")
        
        self.delay_label = tk.Label(
            delay_frame,
            textvariable=self.delay_inicial,
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="#3498db",
            width=6
        )
        self.delay_label.pack(side="left", padx=10)
        
        tk.Label(
            frame_config,
            text="↑ Aumenta si el resaltado va ADELANTADO",
            font=("Arial", 9, "italic"),
            bg="#2c3e50",
            fg="#95a5a6"
        ).grid(row=1, column=1, sticky="w", padx=10)
        
        # Factor Longitud
        tk.Label(
            frame_config,
            text="📏 Factor Longitud Palabra:",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#ecf0f1"
        ).grid(row=2, column=0, sticky="w", pady=(15, 5))
        
        factor_frame = tk.Frame(frame_config, bg="#2c3e50")
        factor_frame.grid(row=2, column=1, sticky="ew", padx=10, pady=(15, 0))
        
        self.factor_scale = tk.Scale(
            factor_frame,
            from_=0.01,
            to=0.05,
            resolution=0.005,
            orient="horizontal",
            variable=self.factor_longitud,
            bg="#34495e",
            fg="#ecf0f1",
            highlightthickness=0,
            length=250
        )
        self.factor_scale.pack(side="left")
        
        self.factor_label = tk.Label(
            factor_frame,
            textvariable=self.factor_longitud,
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="#3498db",
            width=6
        )
        self.factor_label.pack(side="left", padx=10)
        
        tk.Label(
            frame_config,
            text="↑ Ajusta el tiempo extra para palabras largas",
            font=("Arial", 9, "italic"),
            bg="#2c3e50",
            fg="#95a5a6"
        ).grid(row=3, column=1, sticky="w", padx=10)
        
        # Frame de prueba
        frame_prueba = tk.LabelFrame(
            self.root,
            text="🎤 Texto de Prueba",
            font=("Arial", 12, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
            padx=15,
            pady=10
        )
        frame_prueba.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.texto = tk.Text(
            frame_prueba,
            font=("Arial", 11),
            bg="#ecf0f1",
            fg="#2c3e50",
            wrap="word",
            height=10,
            padx=10,
            pady=10
        )
        self.texto.pack(fill="both", expand=True)
        
        # Texto de prueba predefinido
        texto_prueba = """Prueba de sincronización del sistema de resaltado visual.

Las palabras cortas y las palabras más largas deben resaltarse exactamente cuando se pronuncian.

Observa cuidadosamente la sincronización entre el resaltado amarillo y la voz del sistema."""
        
        self.texto.insert("1.0", texto_prueba)
        
        # Frame de botones
        frame_botones = tk.Frame(self.root, bg="#34495e")
        frame_botones.pack(pady=15)
        
        # Botón probar
        self.btn_probar = tk.Button(
            frame_botones,
            text="🎤 Probar Sincronización",
            font=("Arial", 13, "bold"),
            bg="#27ae60",
            fg="white",
            padx=25,
            pady=12,
            command=self.probar_sincronizacion,
            cursor="hand2"
        )
        self.btn_probar.pack(side="left", padx=5)
        
        # Botón guardar
        btn_guardar = tk.Button(
            frame_botones,
            text="💾 Guardar Configuración",
            font=("Arial", 13, "bold"),
            bg="#3498db",
            fg="white",
            padx=25,
            pady=12,
            command=self.guardar_configuracion,
            cursor="hand2"
        )
        btn_guardar.pack(side="left", padx=5)
        
        # Botón restaurar
        btn_restaurar = tk.Button(
            frame_botones,
            text="🔄 Restaurar Valores",
            font=("Arial", 13, "bold"),
            bg="#e67e22",
            fg="white",
            padx=25,
            pady=12,
            command=self.restaurar_valores,
            cursor="hand2"
        )
        btn_restaurar.pack(side="left", padx=5)
        
        # Estado
        self.label_estado = tk.Label(
            self.root,
            text="Ajusta los valores y prueba la sincronización",
            font=("Arial", 10),
            bg="#34495e",
            fg="#3498db"
        )
        self.label_estado.pack(pady=10)
        
        # Instrucciones
        instrucciones = tk.Label(
            self.root,
            text="💡 Consejo: Si el resaltado va adelantado, aumenta el Delay Inicial. "
                 "Si va atrasado, disminúyelo.",
            font=("Arial", 9, "italic"),
            bg="#34495e",
            fg="#95a5a6",
            wraplength=800
        )
        instrucciones.pack(pady=5)
        
    def probar_sincronizacion(self):
        """Prueba la sincronización con los valores actuales"""
        # Guardar temporalmente los valores
        self.aplicar_configuracion_temporal()
        
        # Crear operativo con widget
        if not self.operativo:
            self.operativo = Operativo()
            self.operativo.set_texto_widget(self.texto)
        
        texto_contenido = self.texto.get("1.0", END)
        
        self.btn_probar.config(state="disabled")
        self.label_estado.config(
            text="🔊 Reproduciendo... Observa si el resaltado está sincronizado",
            fg="#f39c12"
        )
        
        import threading
        def probar():
            try:
                self.operativo.leerArchivo(texto_contenido)
            finally:
                self.root.after(0, self.finalizar_prueba)
        
        thread = threading.Thread(target=probar, daemon=True)
        thread.start()
    
    def finalizar_prueba(self):
        """Restaura la interfaz después de la prueba"""
        self.btn_probar.config(state="normal")
        self.label_estado.config(
            text="✅ Prueba completada. ¿Estuvo sincronizado? Ajusta si es necesario.",
            fg="#27ae60"
        )
    
    def aplicar_configuracion_temporal(self):
        """Aplica la configuración actual temporalmente"""
        import config_resaltado
        config_resaltado.DELAY_INICIAL = self.delay_inicial.get()
        config_resaltado.FACTOR_LONGITUD_PALABRA = self.factor_longitud.get()
        
        # Recargar el módulo Proceso para que use los nuevos valores
        import importlib
        import Proceso
        importlib.reload(Proceso)
        
        # Recrear operativo
        self.operativo = Proceso.Operativo()
        self.operativo.set_texto_widget(self.texto)
    
    def guardar_configuracion(self):
        """Guarda la configuración en el archivo"""
        delay = self.delay_inicial.get()
        factor = self.factor_longitud.get()
        
        contenido = f'''"""
Configuración de sincronización del resaltado de palabras
Ajusta estos valores si el resaltado no está perfectamente sincronizado con la voz
"""

# ============================================
# CONFIGURACIÓN DE SINCRONIZACIÓN
# ============================================

# Delay inicial antes de empezar el resaltado (en segundos)
DELAY_INICIAL = {delay}

# Factor de ajuste de longitud de palabra
FACTOR_LONGITUD_PALABRA = {factor}

# Umbral de longitud para aplicar factor
UMBRAL_PALABRA_LARGA = 5

# Delay final para limpiar resaltado (en segundos)
DELAY_LIMPIEZA = 0.3

# ============================================
# NOTAS
# ============================================
# Estos valores fueron ajustados usando el Calibrador de Sincronización
# Si necesitas reajustar, ejecuta: python calibrar_sincronizacion.py
'''
        
        try:
            with open('config_resaltado.py', 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            self.label_estado.config(
                text=f"✅ Configuración guardada: Delay={delay}s, Factor={factor}",
                fg="#27ae60"
            )
        except Exception as e:
            self.label_estado.config(
                text=f"❌ Error al guardar: {e}",
                fg="#e74c3c"
            )
    
    def restaurar_valores(self):
        """Restaura los valores predeterminados"""
        self.delay_inicial.set(0.15)
        self.factor_longitud.set(0.02)
        self.label_estado.config(
            text="🔄 Valores restaurados a predeterminados",
            fg="#3498db"
        )
    
    def ejecutar(self):
        print("=" * 70)
        print("  CALIBRADOR DE SINCRONIZACIÓN - Resaltado Visual TTS")
        print("=" * 70)
        print()
        print("Este calibrador te ayuda a ajustar la sincronización del resaltado")
        print("para que coincida perfectamente con la voz del TTS.")
        print()
        print("Instrucciones:")
        print("1. Ajusta el 'Delay Inicial' y 'Factor Longitud Palabra'")
        print("2. Presiona '🎤 Probar Sincronización'")
        print("3. Observa si el resaltado amarillo va a la par de la voz")
        print("4. Si va adelantado: Aumenta el Delay Inicial")
        print("5. Si va atrasado: Disminuye el Delay Inicial")
        print("6. Cuando esté perfecto: Presiona '💾 Guardar Configuración'")
        print()
        print("Valores actuales:")
        print(f"  - Delay Inicial: {self.delay_inicial.get()}s")
        print(f"  - Factor Longitud: {self.factor_longitud.get()}")
        print()
        print("=" * 70)
        
        self.root.mainloop()

if __name__ == "__main__":
    calibrador = CalibradorSincronizacion()
    calibrador.ejecutar()
