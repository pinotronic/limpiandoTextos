# Limpiando Texto 4.5

Aplicación de escritorio desarrollada en Python con Tkinter para limpiar y procesar texto de documentos OCR y otros formatos.

## Características

### 🎯 Procesamiento Básico
- **Limpieza automática de texto**: Procesa y mejora texto extraído de documentos OCR
- **Corrección de formato**: Ajusta puntuación, espacios y estructura del texto
- **Conversión de bullets**: Convierte diferentes tipos de viñetas a formato estándar
- **Procesamiento de saltos de línea**: Maneja correctamente los saltos de línea en el texto
- **Interfaz gráfica intuitiva**: Fácil de usar con botones para las operaciones más comunes
- **Síntesis de voz**: Convierte el texto procesado a audio usando gTTS y pyttsx3

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
- pyttsx3
- gTTS (Google Text-to-Speech)

### Para funciones de IA (opcional)
- requests
- API Key de DeepSeek (gratuita)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/pinotronic/limpiandoTextos.git
cd limpiandoTextos
```

2. Instalar dependencias básicas:
```bash
pip install pyperclip pyttsx3 gTTS requests
```

3. **OPCIONAL - Configurar IA DeepSeek:**
   - Copia `config_ia_ejemplo.py` a `config_ia.py`
   - Obtén tu API key gratuita en: https://platform.deepseek.com/
   - Reemplaza `tu_api_key_aqui` con tu API key real en `config_ia.py`

4. Ejecutar la aplicación:
```bash
python limpiandoTexto.pyw
```

## Uso

1. **Cargar texto**: Pega o carga texto en el área de texto principal
2. **Procesar**: Haz clic en el botón 🚀 para aplicar las funciones de limpieza
3. **Sustituir texto**: Usa los campos inferiores para reemplazar texto específico
4. **Copiar resultado**: Usa el botón 📑 para copiar el texto procesado

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