# Script de instalación automática de Piper TTS
# Para usar: .\install_piper.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Instalador de Piper TTS" -ForegroundColor Cyan
Write-Host "  Para Limpiando Texto 4.5" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# URLs de descarga
$piperVersion = "2023.11.14-2"
$piperUrl = "https://github.com/rhasspy/piper/releases/download/$piperVersion/piper_windows_amd64.zip"
$modelBaseUrl = "https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/sharvie/medium"
$modelName = "es_ES-sharvie-medium"

Write-Host "Este script instalará:" -ForegroundColor Yellow
Write-Host "  1. Piper TTS (motor de síntesis de voz)" -ForegroundColor White
Write-Host "  2. Modelo de voz español 'sharvie' (voz femenina, calidad media)" -ForegroundColor White
Write-Host "  3. Tamaño total de descarga: ~50MB" -ForegroundColor White
Write-Host ""

# Verificar si ya está instalado
if (Test-Path "piper\piper.exe") {
    Write-Host "⚠️  Piper TTS ya está instalado" -ForegroundColor Yellow
    $respuesta = Read-Host "¿Deseas reinstalar? (s/N)"
    if ($respuesta -ne "s" -and $respuesta -ne "S") {
        Write-Host "Instalación cancelada" -ForegroundColor Red
        exit
    }
    Write-Host "Eliminando instalación anterior..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force piper -ErrorAction SilentlyContinue
}

Write-Host ""
$confirmacion = Read-Host "¿Deseas continuar con la instalación? (S/n)"
if ($confirmacion -eq "n" -or $confirmacion -eq "N") {
    Write-Host "Instalación cancelada" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Iniciando instalación..." -ForegroundColor Green
Write-Host ""

# Crear directorios
Write-Host "[1/4] Creando directorios..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "piper\models" | Out-Null
Write-Host "      ✅ Directorios creados" -ForegroundColor Green

# Descargar Piper
Write-Host "[2/4] Descargando Piper TTS ($piperVersion)..." -ForegroundColor Cyan
try {
    Invoke-WebRequest -Uri $piperUrl -OutFile "piper.zip" -UseBasicParsing
    Write-Host "      ✅ Piper descargado" -ForegroundColor Green
} catch {
    Write-Host "      ❌ Error al descargar Piper: $_" -ForegroundColor Red
    exit 1
}

# Extraer Piper
Write-Host "[3/4] Extrayendo Piper..." -ForegroundColor Cyan
try {
    Expand-Archive -Path "piper.zip" -DestinationPath "piper" -Force
    Remove-Item "piper.zip"
    Write-Host "      ✅ Piper extraído" -ForegroundColor Green
} catch {
    Write-Host "      ❌ Error al extraer Piper: $_" -ForegroundColor Red
    exit 1
}

# Descargar modelo español
Write-Host "[4/4] Descargando modelo de voz español..." -ForegroundColor Cyan
try {
    # Descargar archivo .onnx (modelo)
    Write-Host "      Descargando $modelName.onnx..." -ForegroundColor Gray
    Invoke-WebRequest -Uri "$modelBaseUrl/$modelName.onnx" `
        -OutFile "piper\models\$modelName.onnx" -UseBasicParsing
    
    # Descargar archivo .onnx.json (configuración)
    Write-Host "      Descargando $modelName.onnx.json..." -ForegroundColor Gray
    Invoke-WebRequest -Uri "$modelBaseUrl/$modelName.onnx.json" `
        -OutFile "piper\models\$modelName.onnx.json" -UseBasicParsing
    
    Write-Host "      ✅ Modelo español descargado" -ForegroundColor Green
} catch {
    Write-Host "      ❌ Error al descargar modelo: $_" -ForegroundColor Red
    Write-Host "      El programa seguirá funcionando con pyttsx3" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  ✅ INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Verificar archivos
Write-Host "Archivos instalados:" -ForegroundColor Cyan
if (Test-Path "piper\piper.exe") {
    Write-Host "  ✅ piper.exe" -ForegroundColor Green
} else {
    Write-Host "  ❌ piper.exe (falta)" -ForegroundColor Red
}

if (Test-Path "piper\models\$modelName.onnx") {
    $size = (Get-Item "piper\models\$modelName.onnx").Length / 1MB
    Write-Host "  ✅ $modelName.onnx ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "  ❌ $modelName.onnx (falta)" -ForegroundColor Red
}

if (Test-Path "piper\models\$modelName.onnx.json") {
    Write-Host "  ✅ $modelName.onnx.json" -ForegroundColor Green
} else {
    Write-Host "  ❌ $modelName.onnx.json (falta)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Estructura de directorios:" -ForegroundColor Cyan
Write-Host "  piper/" -ForegroundColor White
Write-Host "    ├── piper.exe" -ForegroundColor White
Write-Host "    ├── *.dll (librerías)" -ForegroundColor White
Write-Host "    └── models/" -ForegroundColor White
Write-Host "        ├── $modelName.onnx" -ForegroundColor White
Write-Host "        └── $modelName.onnx.json" -ForegroundColor White

Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Reinicia el programa 'Limpiando Texto 4.5'" -ForegroundColor White
Write-Host "  2. Verás en la consola: '✅ Piper TTS detectado'" -ForegroundColor White
Write-Host "  3. Presiona el botón 🔊 para escuchar con alta calidad" -ForegroundColor White

Write-Host ""
Write-Host "¿Deseas probar Piper ahora? (s/N): " -ForegroundColor Cyan -NoNewline
$probar = Read-Host

if ($probar -eq "s" -or $probar -eq "S") {
    Write-Host ""
    Write-Host "Probando Piper TTS..." -ForegroundColor Cyan
    $textoTest = "Hola, esto es una prueba de Piper TTS. Síntesis de voz neuronal de alta calidad."
    
    try {
        $textoTest | & ".\piper\piper.exe" --model ".\piper\models\$modelName.onnx" --output_file "test_piper.wav"
        
        if (Test-Path "test_piper.wav") {
            Write-Host "✅ Audio generado: test_piper.wav" -ForegroundColor Green
            Write-Host "Reproduciendo audio..." -ForegroundColor Cyan
            Start-Process "test_piper.wav"
            Write-Host ""
            Write-Host "Si escuchaste el audio, ¡Piper funciona correctamente!" -ForegroundColor Green
        } else {
            Write-Host "❌ No se pudo generar el audio de prueba" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Error al probar Piper: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Para más información, consulta: INSTALACION_PIPER_TTS.md" -ForegroundColor Gray
Write-Host ""

# Opcional: Mostrar otros modelos disponibles
Write-Host "Modelos adicionales disponibles:" -ForegroundColor Yellow
Write-Host "  - es_ES-davefx-medium (voz masculina)" -ForegroundColor White
Write-Host "  - es_MX-ald-medium (español mexicano)" -ForegroundColor White
Write-Host "  - es_AR-tux-medium (español argentino)" -ForegroundColor White
Write-Host ""
Write-Host "Para descargar otros modelos, visita:" -ForegroundColor Gray
Write-Host "  https://huggingface.co/rhasspy/piper-voices/tree/main/es" -ForegroundColor Gray
Write-Host ""

Write-Host "Presiona Enter para salir..." -ForegroundColor Gray
Read-Host
