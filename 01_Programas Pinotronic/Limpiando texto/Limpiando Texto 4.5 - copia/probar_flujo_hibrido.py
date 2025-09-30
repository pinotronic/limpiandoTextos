"""
Prueba del nuevo flujo: Procesamiento Básico Completo + Refinamiento IA
"""

from Proceso import Operativo

def probar_flujo_hibrido():
    print("🔧 Probando nuevo flujo híbrido...")
    
    procesador = Operativo()
    
    # Texto complejo que prueba todas las funciones
    texto_complejo = """INFORME TÉCNICO
Introduccion al sistema
Este documento contiene informacion importante sobre el funcionamiento del sistema operativo
Los siguientes elementos son criticos:
• Verificar configuracion de red
• Revisar logs del sistema
• Monitorear rendimiento
SECCION 2: Procedimientos
Para realizar el mantenimiento se debe:
1. Detener servicios
2. Hacer respaldo 
3. Aplicar actualizaciones
CONCLUSION
El mantenimiento preventivo es esencial para el correcto funcionarniento del sistema"""

    print("\n" + "="*70)
    print("📝 TEXTO ORIGINAL:")
    print("="*70)
    print(texto_complejo)
    
    print("\n" + "="*70)
    print("🔄 PROCESAMIENTO BÁSICO (sin IA):")
    print("="*70)
    resultado_basico = procesador.realizandoProceso(texto_complejo, usar_ia=False)
    print(resultado_basico)
    
    print("\n" + "="*70)
    print("🧠 PROCESAMIENTO HÍBRIDO (Básico + IA):")
    print("="*70)
    resultado_hibrido = procesador.realizandoProceso(texto_complejo, usar_ia=True)
    print(resultado_hibrido)
    
    print("\n" + "="*70)
    print("📊 COMPARACIÓN:")
    print("="*70)
    print("✅ Básico: Aplica todas las reglas tradicionales")
    print("🧠 Híbrido: Básico + refinamiento inteligente final")
    print("🎯 La IA mejora el resultado SIN romper el procesamiento original")

if __name__ == "__main__":
    probar_flujo_hibrido()