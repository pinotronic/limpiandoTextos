# Limpiando Texto 4.5

Aplicación de escritorio desarrollada en Python con Tkinter para limpiar y procesar texto de documentos OCR y otros formatos.

## Características

### 🎯 Procesamiento Básico
- **Limpieza automática de texto**: Procesa y mejora texto extraído de documentos OCR
- **Corrección de formato**: Ajusta puntuación, espacios y estructura del texto
- **Conversión de bullets**: Convierte diferentes tipos de viñetas a formato estándar
- **Procesamiento de saltos de línea**: Maneja correctamente los saltos de línea en el texto
- **Interfaz gráfica intuitiva**: Fácil de usar con botones para las operaciones más comunes
- **Síntesis de voz OFFLINE**: ¡Funciona sin Internet! Usa voces del sistema (pyttsx3) + opción de alta calidad con Piper TTS

### 🎙️ Síntesis de Voz (TTS)
El programa incluye un **sistema de síntesis de voz inteligente** con soporte completo offline:

- **🥇 Piper TTS** (opcional): Alta calidad neural, completamente offline
- **🥈 pyttsx3** (incluido): Voces del sistema Windows, siempre disponible offline
- **🥉 gTTS** (fallback): Online, solo si hay conexión a Internet

**¡El programa lee texto SIN NECESIDAD de conexión a Internet!** Usa pyttsx3 por defecto (ya incluido).  
Para voces de mayor calidad, puedes instalar Piper TTS (opcional). Ver [INSTALACION_PIPER_TTS.md](INSTALACION_PIPER_TTS.md)

### 🎨 Resaltado Visual de Palabras (NUEVO)
**¡Nueva característica!** Durante la lectura con TTS:

- **✨ Palabras se resaltan** con fondo amarillo mientras se leen
- **🎯 Sincronización perfecta** entre voz y resaltado visual
- **📜 Scroll automático** para seguir la lectura
- **⏹ Control de lectura** con botón de detener
- **♿ Mejora accesibilidad** - ideal para dislexia y aprendizaje

**Beneficios:**
- Mejor comprensión del texto
- Seguimiento visual de la lectura
- Herramienta de aprendizaje
- Mayor concentración

Ver documentación completa: [RESALTADO_PALABRAS.md](RESALTADO_PALABRAS.md)

### 🧠 Procesamiento con IA (DeepSeek)
- **Corrección inteligente de errores OCR**: Detecta y corrige automáticamente errores típicos
- **Análisis contextual**: Entiende el tipo de documento y ajusta el procesamiento
- **Puntuación inteligente**: No agrega puntos incorrectos delante de títulos o nombres propios
- **Preservación de formato**: Mantiene la estructura original cuando es apropiada
- **Procesamiento híbrido**: Combina reglas tradicionales con IA para mejores resultados

## Archivos del proyecto

- `limpiandoTexto.pyw`: Archivo principal con la interfaz gráfica
- `Proceso.py`: Clase con las funciones de procesamiento de texto
- `ManejoArchivos.py`: Clase para manejo de archivos (cargar/guardar)
- `vista.tcl`: Archivo de configuración de la interfaz (PAGE)
- `Dockerfile`: Configuración para contenedor Docker
- `escoba.ico`, `icon.ico`: Iconos de la aplicación

## Requisitos

### Básicos (obligatorios)
- Python 3.x
- tkinter (incluido con Python)
- pyperclip
- pyttsx3 (TTS offline - voces del sistema)

### Opcionales (mejoras)
- **gTTS** (Google Text-to-Speech) - Solo para TTS online si tienes Internet
- **Piper TTS** - Alta calidad neural offline (ver [INSTALACION_PIPER_TTS.md](INSTALACION_PIPER_TTS.md))
- **requests** - Para funciones de IA
- **API Key de DeepSeek** - Gratuita, para procesamiento con IA

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/pinotronic/limpiandoTextos.git
cd limpiandoTextos
```

2. Instalar dependencias básicas:
```bash
# Dependencias mínimas (programa funciona completamente offline)
pip install pyperclip pyttsx3

# Opcionales: gTTS para online y requests para IA
pip install gTTS requests
```

3. **OPCIONAL - TTS de Alta Calidad (Piper):**
   - Ver guía completa en: [INSTALACION_PIPER_TTS.md](INSTALACION_PIPER_TTS.md)
   - Piper TTS ofrece voces neuronales de alta calidad completamente offline
   - No es necesario para el funcionamiento básico (pyttsx3 ya funciona offline)

4. **OPCIONAL - Configurar IA DeepSeek:**
   - Copia `config_ia_ejemplo.py` a `config_ia.py`
   - Obtén tu API key gratuita en: https://platform.deepseek.com/
   - Reemplaza `tu_api_key_aqui` con tu API key real en `config_ia.py`

5. Ejecutar la aplicación:
```bash
python limpiandoTexto.pyw
```

## Uso

1. **Cargar texto**: Pega o carga texto en el área de texto principal
2. **Procesar**: Haz clic en el botón 🚀 para aplicar las funciones de limpieza
3. **Leer texto**: Usa el botón 🔊 para escuchar el texto (funciona offline con pyttsx3)
4. **Sustituir texto**: Usa los campos inferiores para reemplazar texto específico
5. **Copiar resultado**: Usa el botón 📑 para copiar el texto procesado

### Botones principales
- 🚀 **Procesar**: Aplica limpieza automática del texto
- 📑 **Copiar**: Copia el texto procesado al portapapeles
- 🔊 **Leer**: Lee el texto en voz alta (OFFLINE por defecto) con resaltado visual
- ⏹ **Detener**: Detiene la lectura en curso (aparece durante la lectura)
- 🗑 **Borrar**: Limpia el área de texto
- 📁 **Abrir**: Carga un archivo de texto
- 💾 **Guardar**: Guarda el texto en un archivo
- 🔒 **Salir**: Cierra la aplicación
- ➕ **Cambiar**: Sustituye texto personalizado

### Nueva característica: Resaltado Visual
Cuando presionas 🔊 (Leer):
1. Las palabras se resaltan en **amarillo** mientras se leen
2. El resaltado se sincroniza con la voz
3. El scroll sigue automáticamente la lectura
4. Puedes detener en cualquier momento con ⏹

## Funciones de procesamiento

- Corrección de comas y espacios
- Conversión de bullets y viñetas
- Manejo inteligente de puntuación
- Limpieza de saltos de línea innecesarios
- Formateo de números e incisos
- Inserción estratégica de saltos de línea

## Historial de cambios

### Versión 4.5
- **Fix**: Desactivada función que colocaba puntos incorrectos delante de letras mayúsculas
- Mejoras en el procesamiento de texto para preservar formato original
- Correcciones en el manejo de títulos y nombres propios

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Autor

**Pinotronic** - [GitHub](https://github.com/pinotronic)