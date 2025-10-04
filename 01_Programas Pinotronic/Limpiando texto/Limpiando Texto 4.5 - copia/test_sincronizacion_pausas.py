"""
Script de prueba para verificar la sincronización de pausas de puntuación
Crea un texto de prueba con comas, puntos y saltos de línea
"""

import tkinter as tk
from Proceso import Operativo
import time

# Texto de prueba con múltiples tipos de puntuación
TEXTO_PRUEBA = """Hola, este es un texto de prueba.
Tiene varias líneas para verificar las pausas correctas.
Las comas, puntos y saltos de línea, deben sincronizarse perfectamente con la voz.
Cada pausa debe ser respetada por el resaltado visual.
¡Gracias por probar este sistema!"""

def main():
    # Crear ventana de prueba
    root = tk.Tk()
    root.title("Prueba de Sincronización con Pausas")
    root.geometry("600x400")
    
    # Crear widget de texto
    texto_widget = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), padx=10, pady=10)
    texto_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    texto_widget.insert("1.0", TEXTO_PRUEBA)
    
    # Crear instancia del operativo
    operativo = Operativo()
    operativo.set_texto_widget(texto_widget)
    
    # Botón para iniciar lectura
    def iniciar_lectura():
        print("\n" + "="*60)
        print("INICIANDO PRUEBA DE SINCRONIZACIÓN")
        print("="*60)
        print(f"\nTexto a leer ({len(TEXTO_PRUEBA.split())} palabras):")
        print(f"- Comas: {TEXTO_PRUEBA.count(',')}")
        print(f"- Puntos: {TEXTO_PRUEBA.count('.')}")
        print(f"- Saltos de línea: {TEXTO_PRUEBA.count(chr(10))}")
        print("\n✅ Observa que el resaltado RESPETA las pausas de puntuación")
        print("✅ El resaltado debe terminar AL MISMO TIEMPO que la voz\n")
        
        # Iniciar lectura en hilo separado para no bloquear UI
        import threading
        def leer():
            operativo.leerArchivo(TEXTO_PRUEBA)
        
        hilo = threading.Thread(target=leer, daemon=True)
        hilo.start()
    
    def detener_lectura():
        operativo.detener_lectura()
        print("\n⏹ Lectura detenida")
    
    # Frame para botones
    frame_botones = tk.Frame(root)
    frame_botones.pack(pady=10)
    
    btn_leer = tk.Button(frame_botones, text="▶ INICIAR LECTURA", command=iniciar_lectura, 
                         bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
    btn_leer.pack(side=tk.LEFT, padx=5)
    
    btn_detener = tk.Button(frame_botones, text="⏹ DETENER", command=detener_lectura,
                           bg="#f44336", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
    btn_detener.pack(side=tk.LEFT, padx=5)
    
    # Instrucciones
    instrucciones = tk.Label(root, text="Observa cómo el resaltado respeta las pausas de comas, puntos y saltos de línea",
                            font=("Arial", 10, "italic"), fg="gray")
    instrucciones.pack(pady=5)
    
    print("\n" + "="*60)
    print("VENTANA DE PRUEBA ABIERTA")
    print("="*60)
    print("\nInstrucciones:")
    print("1. Haz clic en 'INICIAR LECTURA'")
    print("2. Observa que el resaltado hace pausas en:")
    print("   - Comas (0.25s)")
    print("   - Puntos (0.35s)")
    print("   - Saltos de línea (0.40s)")
    print("3. Verifica que el resaltado termina AL MISMO TIEMPO que la voz")
    print("\n⚠️ Si aún hay desincronización, ajusta config_resaltado.py")
    
    root.mainloop()

if __name__ == "__main__":
    main()
