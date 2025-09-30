# Configuración EJEMPLO para la API de DeepSeek
# INSTRUCCIONES PARA USAR LA IA:
# 
# 1. Copia este archivo y renómbralo a 'config_ia.py'
# 2. Reemplaza 'tu_api_key_aqui' con tu API key real de DeepSeek
# 3. El archivo config_ia.py NO se subirá al repositorio por seguridad
#
# Para obtener tu API key:
# - Ve a https://platform.deepseek.com/
# - Regístrate o inicia sesión
# - Ve a API Keys y crea una nueva clave

DEEPSEEK_API_KEY = "tu_api_key_aqui"

# Configuraciones adicionales de IA
IA_CONFIG = {
    "habilitada": True,           # Habilitar/deshabilitar IA globalmente
    "modo_debug": False,          # Mostrar información detallada de debug
    "timeout": 30,                # Tiempo límite para llamadas a API (segundos)
    "max_tokens": 2000,           # Máximo tokens en respuesta
    "temperature": 0.1,           # Creatividad de la IA (0.0-1.0, menor = más consistente)
    "usar_cache": True,           # Cache de respuestas para texto repetitivo
    "fallback_a_basico": True     # Si IA falla, usar procesamiento básico
}