"""
Script de prueba avanzada con texto OCR real
"""

from Proceso import Operativo

def probar_texto_complejo():
    print("🔧 Probando con texto OCR complejo...")
    
    procesador = Operativo()
    
    # Texto que simula errores típicos de OCR
    texto_ocr = """MANUAL DE USUARIO
Capitulo 1: lntroducción
Este es un texto que ha sido procesado por OCR y contiene errores tipicos
corno la confusión entre 'rn' y 'm' en paiabras corno 'corno' en lugar de 'como'
Tambien hay espacios extras   y  saltos de linea 
incorrectos
SECCION A
Punto importante: las letras 'cl' a menudo se leen como 'd'
Lista de items:
• Primer elemento
• Segundo eiemento 
• Tercer elemento con errores tipicos
CONCLUSION
El procesarniento debe mejorar estos errores automaticamente"""

    print("📝 Texto OCR original (con errores típicos):")
    print("=" * 60)
    print(texto_ocr)
    print("=" * 60)
    
    print("\n🔄 Procesando con IA...")
    resultado = procesador.realizandoProceso(texto_ocr, usar_ia=True)
    
    print("\n✨ Texto procesado con IA:")
    print("=" * 60)
    print(resultado)
    print("=" * 60)
    
    print("\n🎯 ¡Prueba completada! La IA debería haber:")
    print("   ✅ Corregido errores de OCR (rn→m, cl→d)")
    print("   ✅ Mantenido títulos sin puntos incorrectos")
    print("   ✅ Mejorado el formato y fluidez")
    print("   ✅ Preservado la estructura del documento")

if __name__ == "__main__":
    probar_texto_complejo()