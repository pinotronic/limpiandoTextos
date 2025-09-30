"""
Test del sistema de progreso con IA
"""

from Proceso import Operativo

# Función de callback para mostrar progreso
def mostrar_progreso(mensaje):
    print(f"🔄 PROGRESO: {mensaje}")

# Crear instancia del operativo
operativo = Operativo()

# Configurar callback
operativo.set_callback_progreso(mostrar_progreso)

# Habilitar IA
operativo.habilitar_ia()

print("=== PRUEBA DE PROGRESO CON IA ===")
print(f"IA disponible: {operativo.ia_habilitada}")

# Texto de prueba
texto_prueba = """ESTE ES UN EJEMPLO DE TEXTO CON ERRORES.
El texto tiene algunas. palabras mal separadas
y puede tener errores de OCR comunes."""

print("\n=== INICIANDO PROCESAMIENTO ===")

# Procesar con IA (incluye progreso)
resultado = operativo.realizandoProceso(texto_prueba)

print("\n=== RESULTADO FINAL ===")
print(resultado[:200] + "..." if len(resultado) > 200 else resultado)