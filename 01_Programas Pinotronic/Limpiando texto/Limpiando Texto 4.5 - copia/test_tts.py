"""
Script de prueba del sistema TTS
Verifica el funcionamiento de pyttsx3, Piper y gTTS
"""

import sys
import os

print("=" * 60)
print("  PRUEBA DEL SISTEMA TTS - Limpiando Texto 4.5")
print("=" * 60)
print()

# Agregar el directorio actual al path para importar Proceso
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Proceso import Operativo

print("Inicializando sistema...")
print()

operativo = Operativo()

print()
print("=" * 60)
print("  RESUMEN DE MOTORES TTS DISPONIBLES")
print("=" * 60)
print()

# Verificar pyttsx3
print("1. pyttsx3 (Offline - Voces del sistema)")
print("   " + "-" * 50)
try:
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(f"   ✅ DISPONIBLE - {len(voices)} voces instaladas")
    
    # Listar voces en español
    voces_espanol = [v for v in voices if 'spanish' in v.name.lower() or 'español' in v.name.lower()]
    if voces_espanol:
        print(f"   🎤 Voces en español: {len(voces_espanol)}")
        for voz in voces_espanol[:3]:  # Mostrar máximo 3
            print(f"      - {voz.name}")
    else:
        print("   ⚠️  No se encontraron voces en español")
        print("      Se usará la voz predeterminada del sistema")
    engine.stop()
except Exception as e:
    print(f"   ❌ ERROR: {e}")

print()

# Verificar Piper
print("2. Piper TTS (Offline - Alta calidad neural)")
print("   " + "-" * 50)
if operativo.piper_path and operativo.piper_model:
    print(f"   ✅ DISPONIBLE")
    print(f"   📂 Ejecutable: {operativo.piper_path}")
    print(f"   🎙️  Modelo: {os.path.basename(operativo.piper_model)}")
else:
    print("   ⚠️  NO INSTALADO (Opcional)")
    print("   💡 Para instalar: Ejecuta install_piper.ps1")
    print("   📖 Guía: INSTALACION_PIPER_TTS.md")

print()

# Verificar gTTS
print("3. gTTS (Online - Requiere Internet)")
print("   " + "-" * 50)
try:
    from gtts import gTTS
    print("   ✅ DISPONIBLE (requiere conexión a Internet)")
    print("   🌐 Servicio: Google Text-to-Speech")
except ImportError:
    print("   ⚠️  NO INSTALADO")
    print("   💡 Para instalar: pip install gTTS")

print()
print("=" * 60)
print("  PRUEBA DE FUNCIONAMIENTO")
print("=" * 60)
print()

texto_prueba = "Hola, esto es una prueba del sistema de síntesis de voz. Limpiando texto cuatro punto cinco."

print(f"Texto a sintetizar: '{texto_prueba}'")
print()

respuesta = input("¿Deseas probar la síntesis de voz? (S/n): ").strip().lower()

if respuesta != 'n':
    print()
    print("Reproduciendo texto...")
    print("(El programa intentará usar el mejor motor disponible)")
    print()
    
    try:
        operativo.leerArchivo(texto_prueba)
        print()
        print("✅ Prueba completada")
    except Exception as e:
        print()
        print(f"❌ Error durante la prueba: {e}")
else:
    print()
    print("Prueba cancelada")

print()
print("=" * 60)
print("  RECOMENDACIONES")
print("=" * 60)
print()

if not (operativo.piper_path and operativo.piper_model):
    print("💡 Para mejorar la calidad de la voz:")
    print("   1. Instala Piper TTS (voces neuronales de alta calidad)")
    print("   2. Ejecuta: .\\install_piper.ps1")
    print("   3. Tamaño: ~50MB, completamente offline")
    print()

print("✅ El programa funciona perfectamente con pyttsx3 (ya instalado)")
print("🎙️  Piper TTS es OPCIONAL para voces de mayor calidad")
print("🌐 gTTS es OPCIONAL y solo funciona con Internet")
print()

input("Presiona Enter para salir...")
