# 🎙️ Instalación de Piper TTS (Opcional - Alta Calidad Offline)

Piper TTS es un motor de síntesis de voz **completamente offline** de alta calidad neural. Esta guía te ayudará a instalarlo como opción avanzada para "Limpiando Texto 4.5".

## ¿Por qué Piper TTS?

✅ **Completamente offline** - No requiere conexión a Internet  
✅ **Alta calidad** - Voces neuronales naturales  
✅ **Rápido** - Procesamiento eficiente en CPU  
✅ **Múltiples voces** - Varias opciones en español  
✅ **Gratuito** - Código abierto (MIT License)  
✅ **Ligero** - ~50MB con modelo incluido  

## Sistema de TTS Actual (Sin Piper)

El programa **ya funciona perfectamente offline** usando **pyttsx3**:
- 🎯 **Prioridad 1**: pyttsx3 (ya instalado, voces de Windows)
- 🌐 **Fallback**: gTTS (solo si hay Internet)

**Piper TTS es OPCIONAL** - solo instálalo si quieres voces de mayor calidad.

## Instalación de Piper TTS

### Opción 1: Instalación Automática (Recomendada)

1. **Descarga Piper para Windows**:
   - Ve a: https://github.com/rhasspy/piper/releases/latest
   - Descarga: `piper_windows_amd64.zip` (o la versión para tu arquitectura)

2. **Extrae en el directorio del programa**:
   ```powershell
   # Desde la carpeta del programa
   mkdir piper
   # Extrae el contenido del ZIP en la carpeta 'piper'
   ```

3. **Descarga un modelo de voz en español**:
   - Ve a: https://huggingface.co/rhasspy/piper-voices/tree/main/es
   - Modelos recomendados para español:
     * **es_ES-sharvie-medium** (calidad media, rápida)
     * **es_ES-davefx-medium** (voz masculina natural)
     * **es_MX-ald-medium** (español mexicano)

4. **Descarga los archivos del modelo**:
   Para cada modelo necesitas 2 archivos:
   - `es_ES-sharvie-medium.onnx` (archivo del modelo)
   - `es_ES-sharvie-medium.onnx.json` (configuración)

5. **Estructura final**:
   ```
   Limpiando Texto 4.5 - copia/
   ├── limpiandoTexto.pyw
   ├── Proceso.py
   └── piper/
       ├── piper.exe
       ├── espeak-ng.dll
       ├── onnxruntime.dll
       ├── piper_phonemize.dll
       └── models/
           ├── es_ES-sharvie-medium.onnx
           └── es_ES-sharvie-medium.onnx.json
   ```

### Opción 2: Script de Instalación Automática

Crea y ejecuta este script PowerShell:

```powershell
# install_piper.ps1
$piperUrl = "https://github.com/rhasspy/piper/releases/latest/download/piper_windows_amd64.zip"
$modelUrl = "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/sharvie/medium/es_ES-sharvie-medium.onnx"
$configUrl = "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/sharvie/medium/es_ES-sharvie-medium.onnx.json"

# Crear directorios
New-Item -ItemType Directory -Force -Path "piper\models"

# Descargar Piper
Write-Host "Descargando Piper TTS..."
Invoke-WebRequest -Uri $piperUrl -OutFile "piper.zip"
Expand-Archive -Path "piper.zip" -DestinationPath "piper" -Force
Remove-Item "piper.zip"

# Descargar modelo español
Write-Host "Descargando modelo de voz español..."
Invoke-WebRequest -Uri $modelUrl -OutFile "piper\models\es_ES-sharvie-medium.onnx"
Invoke-WebRequest -Uri $configUrl -OutFile "piper\models\es_ES-sharvie-medium.onnx.json"

Write-Host "✅ Piper TTS instalado correctamente!"
Write-Host "Reinicia el programa para usar Piper TTS"
```

### Opción 3: Piper en PATH del sistema

Si prefieres tener Piper disponible globalmente:

1. Instala Piper en `C:\Program Files\Piper`
2. Agrega `C:\Program Files\Piper` a tu PATH del sistema
3. El programa lo detectará automáticamente

## Verificación de Instalación

Al iniciar el programa, verás en la consola:

```
✅ Piper TTS detectado: es_ES-sharvie-medium.onnx
🎙️ TTS disponibles: pyttsx3 (predeterminado), Piper (alta calidad)
```

Si no ves este mensaje, Piper no fue detectado (el programa seguirá funcionando con pyttsx3).

## Uso

Una vez instalado Piper:

1. **Automático**: El programa intentará usar Piper primero (si está disponible)
2. **Fallback**: Si Piper falla, usará pyttsx3
3. **Online**: Solo usará gTTS si estás conectado y los anteriores fallan

### Orden de Prioridad:
1. 🥇 **Piper TTS** (offline, alta calidad) - Si está instalado
2. 🥈 **pyttsx3** (offline, voces Windows) - Predeterminado
3. 🥉 **gTTS** (online) - Solo con Internet

## Modelos de Voz Recomendados

### Español de España
- **es_ES-sharvie-medium** (22kHz, voz femenina natural) ⭐ Recomendado
- **es_ES-davefx-medium** (22kHz, voz masculina)

### Español Latinoamericano
- **es_MX-ald-medium** (español mexicano, voz masculina)
- **es_AR-tux-medium** (español argentino)

### Descarga de modelos adicionales
https://huggingface.co/rhasspy/piper-voices/tree/main/es

Cada modelo tiene diferentes calidades:
- **low**: ~20MB, rápido pero menos natural
- **medium**: ~50MB, balance calidad/velocidad ⭐
- **high**: ~100MB+, máxima calidad pero más lento

## Prueba de Funcionamiento

Ejecuta este comando en PowerShell desde la carpeta del programa:

```powershell
# Probar Piper directamente
echo "Hola, esto es una prueba de Piper TTS" | .\piper\piper.exe --model .\piper\models\es_ES-sharvie-medium.onnx --output_file test.wav
# Reproducir el archivo generado
.\test.wav
```

## Troubleshooting

### "No se detecta Piper"
- Verifica que `piper.exe` esté en la carpeta `piper/`
- Verifica que el modelo `.onnx` esté en `piper/models/`
- Asegúrate de que ambos archivos (.onnx y .onnx.json) estén presentes

### "DLL no encontrada"
- Asegúrate de extraer TODOS los archivos del ZIP de Piper
- Necesitas: `piper.exe`, `espeak-ng.dll`, `onnxruntime.dll`, `piper_phonemize.dll`

### "Piper tarda mucho"
- Usa un modelo "medium" en lugar de "high"
- Los modelos "low" son más rápidos pero menos naturales

### "Error al ejecutar Piper"
- Verifica que el archivo .onnx.json exista junto al modelo
- Algunos antivirus bloquean binarios descargados - agrega excepción

## Desinstalación

Para remover Piper TTS:

```powershell
# Simplemente elimina la carpeta
Remove-Item -Recurse -Force piper
```

El programa volverá automáticamente a usar pyttsx3.

## Referencias

- **Piper GitHub**: https://github.com/rhasspy/piper
- **Modelos de voz**: https://huggingface.co/rhasspy/piper-voices
- **Documentación oficial**: https://rhasspy.github.io/piper-samples/

## Alternativas Offline Avanzadas

Si quieres experimentar con otras opciones (requieren más configuración):

### Coqui TTS
```bash
pip install TTS
# Usar modelo español
tts --text "Hola mundo" --model_name tts_models/es/css10/vits --out_path output.wav
```

### Kokoro TTS (Ligero)
```bash
pip install kokoro-onnx
# Modelo de 82M parámetros, muy rápido
```

Estas alternativas son más complejas y están fuera del scope de esta guía, pero están disponibles si deseas explorar.

---

**Nota**: Piper TTS es completamente opcional. El programa funciona perfectamente con pyttsx3 (ya incluido) en modo offline. Instala Piper solo si deseas voces de mayor calidad.
