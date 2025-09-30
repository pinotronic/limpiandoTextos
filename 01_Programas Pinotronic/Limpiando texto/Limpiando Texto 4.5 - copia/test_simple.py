"""
Script simple para probar el funcionamiento de la aplicación
"""

import sys
sys.path.append('.')

try:
    print("🔧 Importando módulos...")
    from Proceso import Operativo
    print("✅ Módulo Proceso importado correctamente")
    
    print("🔧 Inicializando procesador...")
    procesador = Operativo()
    print("✅ Procesador inicializado")
    
    # Verificar estado IA
    estado = procesador.estado_ia()
    print(f"📊 Estado IA: {estado}")
    
    # Prueba básica
    texto_prueba = "Hola mundo\nEste es un texto de prueba"
    print(f"📝 Probando con: '{texto_prueba}'")
    
    resultado = procesador.realizandoProceso(texto_prueba)
    print(f"✅ Resultado: '{resultado}'")
    
    print("🎉 ¡Todo funciona correctamente!")
    print("\n🚀 Para ejecutar la aplicación completa:")
    print("   python limpiandoTexto.pyw")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("💡 Solución: Instala las dependencias con 'pip install -r requirements.txt'")
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Revisa la configuración en config_ia.py")
