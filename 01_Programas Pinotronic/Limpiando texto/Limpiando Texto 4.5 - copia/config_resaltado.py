"""
Configuración de sincronización del resaltado de palabras
Ajusta estos valores si el resaltado no está perfectamente sincronizado con la voz
"""

# ============================================
# CONFIGURACIÓN DE SINCRONIZACIÓN
# ============================================

# Delay inicial antes de empezar el resaltado (en segundos)
# Aumenta si el resaltado empieza antes que la voz
# Disminuye si el resaltado empieza tarde
DELAY_INICIAL = 0.15  # Predeterminado: 0.15 segundos

# Factor de ajuste de longitud de palabra
# Controla cuánto más tiempo toman las palabras largas
# Valor más alto = palabras largas se resaltan más tiempo
FACTOR_LONGITUD_PALABRA = 0.02  # Predeterminado: 0.02

# Umbral de longitud para aplicar factor
# Palabras con más caracteres que este valor se consideran "largas"
UMBRAL_PALABRA_LARGA = 5  # Predeterminado: 5 caracteres

# Delay final para limpiar resaltado (en segundos)
# Tiempo de espera antes de limpiar el último resaltado
DELAY_LIMPIEZA = 0.3  # Predeterminado: 0.3 segundos

# ============================================
# PAUSAS DE PUNTUACIÓN
# ============================================

# Tiempo extra después de salto de línea (Enter)
# La voz hace una pausa larga entre párrafos
PAUSA_SALTO_LINEA = 0.4  # Predeterminado: 0.4 segundos

# Tiempo extra después de punto final, exclamación, interrogación
# La voz hace una pausa media al terminar una oración
PAUSA_PUNTO = 0.35  # Predeterminado: 0.35 segundos

# Tiempo extra después de coma, punto y coma, dos puntos
# La voz hace una pausa corta entre frases
PAUSA_COMA = 0.25  # Predeterminado: 0.25 segundos

# ============================================
# AJUSTES FINOS (Para expertos)
# ============================================

# Si el resaltado va MÁS RÁPIDO que la voz:
# - Aumenta DELAY_INICIAL (prueba 0.2, 0.25, 0.3)
# - Aumenta FACTOR_LONGITUD_PALABRA (prueba 0.03, 0.04)

# Si el resaltado va MÁS LENTO que la voz:
# - Disminuye DELAY_INICIAL (prueba 0.1, 0.05)
# - Disminuye FACTOR_LONGITUD_PALABRA (prueba 0.015, 0.01)

# Ejemplos de configuraciones:
# ---------------------------

# Configuración RÁPIDA (para voces lentas):
# DELAY_INICIAL = 0.05
# FACTOR_LONGITUD_PALABRA = 0.01

# Configuración LENTA (para voces rápidas):
# DELAY_INICIAL = 0.3
# FACTOR_LONGITUD_PALABRA = 0.04

# Configuración PRECISA (ajuste fino):
# DELAY_INICIAL = 0.15
# FACTOR_LONGITUD_PALABRA = 0.02

# ============================================
# NOTAS IMPORTANTES
# ============================================

# 1. Velocidad de voz:
#    La velocidad está configurada en Proceso.py:
#    engine.setProperty('rate', 125)
#    
#    Valores típicos:
#    - 100: Muy lento
#    - 125: Normal (predeterminado)
#    - 150: Rápido
#    - 175: Muy rápido

# 2. Diferentes voces pueden tener diferentes ritmos:
#    Microsoft Sabina (México) suele ser más rápida
#    Microsoft Helena (España) suele ser más pausada

# 3. La sincronización puede variar según:
#    - Carga del CPU
#    - Longitud del texto
#    - Complejidad de las palabras
#    - Signos de puntuación

# 4. Para mejor sincronización:
#    - Usa textos no muy largos (< 5000 caracteres)
#    - Evita muchos números y símbolos
#    - Cierra aplicaciones que consuman CPU

# ============================================
# CÓMO PROBAR TUS AJUSTES
# ============================================

# 1. Modifica los valores arriba
# 2. Guarda este archivo
# 3. Ejecuta: python demo_resaltado.py
# 4. Observa si mejora la sincronización
# 5. Ajusta nuevamente si es necesario

# ============================================
# RESTAURAR VALORES PREDETERMINADOS
# ============================================

# Si hiciste cambios y quieres volver a los valores originales:
# DELAY_INICIAL = 0.15
# FACTOR_LONGITUD_PALABRA = 0.02
# UMBRAL_PALABRA_LARGA = 5
# DELAY_LIMPIEZA = 0.3
