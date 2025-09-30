"""
Script de prueba para verificar la integración con DeepSeek IA
Ejecuta este script para probar que todo funciona correctamente
"""

from Proceso import Operativo

def probar_ia():
    print("🔧 Inicializando sistema...")
    
    # Crear instancia del procesador
    procesador = Operativo()
    
    # Verificar estado de la IA
    estado = procesador.estado_ia()
    print(f"\n📊 Estado de la IA:")
    print(f"   - Módulos disponibles: {estado['disponible']}")
    print(f"   - IA inicializada: {estado['inicializada']}")
    print(f"   - IA habilitada: {estado['habilitada']}")
    
    if not estado['habilitada']:
        print("\n⚠️  La IA no está habilitada. Posibles causas:")
        print("   1. No has configurado tu API key en config_ia.py")
        print("   2. La API key es incorrecta")
        print("   3. No hay conexión a internet")
        print("\n📝 Para configurar:")
        print("   1. Edita config_ia.py")
        print("   2. Reemplaza 'tu_api_key_aqui' con tu API key real")
        print("   3. Guarda el archivo y ejecuta este script de nuevo")
        return False
    
    # Texto de prueba
    texto_prueba = """Este es un texto de prueba
Para verificar el funcionamiento
Del sistema de IA integrado
¿Funciona correctamente?"""
    
    print(f"\n📝 Texto de prueba:")
    print(f"'{texto_prueba}'")
    
    # Probar procesamiento básico
    print(f"\n🔄 Probando procesamiento básico...")
    resultado_basico = procesador.realizandoProceso(texto_prueba, usar_ia=False)
    print(f"✅ Resultado básico: '{resultado_basico[:100]}...'")
    
    # Probar procesamiento con IA
    print(f"\n🧠 Probando procesamiento con IA...")
    resultado_ia = procesador.realizandoProceso(texto_prueba, usar_ia=True)
    print(f"✅ Resultado con IA: '{resultado_ia[:100]}...'")
    
    print(f"\n🎉 ¡Prueba completada exitosamente!")
    print(f"   - Procesamiento básico: ✅")
    print(f"   - Procesamiento con IA: ✅")
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 PRUEBA DE INTEGRACIÓN CON DEEPSEEK IA")
    print("=" * 50)
    
    try:
        probar_ia()
    except Exception as e:
        print(f"\n❌ Error durante la prueba: {e}")
        print(f"\n🔧 Soluciones:")
        print(f"   1. Verifica tu API key en config_ia.py")
        print(f"   2. Instala dependencias: pip install requests")
        print(f"   3. Verifica conexión a internet")
    
    print("\n" + "=" * 50)