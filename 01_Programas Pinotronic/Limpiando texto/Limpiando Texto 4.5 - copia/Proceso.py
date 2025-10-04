import re
import pyttsx3
import os
import subprocess
import threading
import time
from pathlib import Path

# Importar gTTS (online) como fallback opcional
try:
    from gtts import gTTS
    GTTS_DISPONIBLE = True
except ImportError:
    GTTS_DISPONIBLE = False
    print("⚠️ gTTS no disponible. Solo modo offline.")

# Intentar importar IA
try:
    from ProcesadorIA import ProcesadorDeepSeek
    from config_ia import DEEPSEEK_API_KEY, IA_CONFIG
    IA_DISPONIBLE = True
except ImportError:
    IA_DISPONIBLE = False
    print("Módulos de IA no disponibles. Funcionando en modo básico.")

# Importar configuración de resaltado
try:
    from config_resaltado import (
        DELAY_INICIAL,
        FACTOR_LONGITUD_PALABRA,
        UMBRAL_PALABRA_LARGA,
        DELAY_LIMPIEZA,
        PAUSA_SALTO_LINEA,
        PAUSA_PUNTO,
        PAUSA_COMA
    )
except ImportError:
    # Valores predeterminados si no existe el archivo de configuración
    DELAY_INICIAL = 0.15
    FACTOR_LONGITUD_PALABRA = 0.02
    UMBRAL_PALABRA_LARGA = 5
    DELAY_LIMPIEZA = 0.3
    PAUSA_SALTO_LINEA = 0.4
    PAUSA_PUNTO = 0.35
    PAUSA_COMA = 0.25

class Operativo:
    def __init__(self):
        self.ia_habilitada = False
        self.procesador_ia = None
        self.callback_progreso = None
        
        # Configuración de TTS
        self.motor_tts = "pyttsx3"  # Por defecto: offline
        self.piper_path = None
        self.piper_model = None
        
        # Configuración de resaltado de palabras
        self.texto_widget = None  # Widget de texto donde resaltar
        self.resaltado_activo = False
        self.hilo_lectura = None
        
        # Detectar Piper TTS si está instalado
        self._detectar_piper()
        
        # Inicializar motor TTS offline (pyttsx3)
        self._inicializar_tts_offline()
        
        # Inicializar IA si está disponible
        if IA_DISPONIBLE and IA_CONFIG.get("habilitada", False):
            try:
                if DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "tu_api_key_aqui":
                    self.procesador_ia = ProcesadorDeepSeek(DEEPSEEK_API_KEY)
                    # Validar API key
                    if self.procesador_ia.validar_api_key():
                        self.ia_habilitada = True
                        print("✅ IA DeepSeek inicializada correctamente")
                    else:
                        print("❌ Error: API key de DeepSeek inválida")
                else:
                    print("⚠️ Configura tu API key en config_ia.py")
            except Exception as e:
                print(f"❌ Error al inicializar IA: {e}")
    
    def set_texto_widget(self, widget):
        """Establece el widget de texto para resaltado durante la lectura"""
        self.texto_widget = widget
    
    def _detectar_piper(self):
        """Detecta si Piper TTS está instalado"""
        try:
            # Buscar piper.exe en el directorio del programa o PATH
            piper_local = Path(__file__).parent / "piper" / "piper.exe"
            
            if piper_local.exists():
                self.piper_path = str(piper_local)
                # Buscar modelo español
                model_dir = piper_local.parent / "models"
                if model_dir.exists():
                    # Buscar modelos .onnx para español
                    modelos_es = list(model_dir.glob("es_*.onnx"))
                    if modelos_es:
                        self.piper_model = str(modelos_es[0])
                        print(f"✅ Piper TTS detectado: {modelos_es[0].name}")
                    else:
                        print("⚠️ Piper encontrado pero sin modelos español")
            else:
                # Verificar si piper está en PATH
                result = subprocess.run(["where", "piper"], 
                                      capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    self.piper_path = result.stdout.strip().split('\n')[0]
                    print(f"✅ Piper TTS en PATH: {self.piper_path}")
        except Exception as e:
            pass  # Piper no disponible, usaremos pyttsx3
    
    def _inicializar_tts_offline(self):
        """Inicializa el motor TTS offline (pyttsx3)"""
        try:
            engine_test = pyttsx3.init()
            engine_test.stop()
            print("✅ Motor TTS offline (pyttsx3) disponible")
            
            # Si Piper está disponible, ofrecer como opción
            if self.piper_path and self.piper_model:
                print("🎙️ TTS disponibles: pyttsx3 (predeterminado), Piper (alta calidad)")
            else:
                print("🎙️ TTS disponible: pyttsx3 (offline)")
        except Exception as e:
            print(f"⚠️ Error al inicializar TTS: {e}")
    
    def habilitar_ia(self, habilitar=True):
        """Habilita o deshabilita el uso de IA"""
        if self.procesador_ia and IA_DISPONIBLE:
            self.ia_habilitada = habilitar
            return True
        return False
    
    def estado_ia(self):
        """Retorna el estado actual de la IA"""
        return {
            "disponible": IA_DISPONIBLE,
            "inicializada": self.procesador_ia is not None,
            "habilitada": self.ia_habilitada
        }
    
    def set_callback_progreso(self, callback):
        """Establece la función callback para notificar progreso"""
        self.callback_progreso = callback
    
    def _notificar_progreso(self, mensaje):
        """Notifica progreso al callback si existe"""
        if self.callback_progreso:
            self.callback_progreso(mensaje)
    
    def sustitucionTexto(self,textoOriginal,texto1,texto2):
        return textoOriginal.replace(texto1, texto2)
    
    def realizandoProceso(self,Textos, usar_ia=None):
        """
        Procesa el texto usando modo básico o IA según configuración
        
        Args:
            Textos (str): Texto a procesar
            usar_ia (bool, optional): Forzar uso de IA (True/False) o usar configuración actual (None)
            
        Returns:
            str: Texto procesado
        """
        # Determinar si usar IA
        if usar_ia is None:
            usar_ia = self.ia_habilitada
        elif usar_ia and not self.ia_habilitada:
            print("⚠️ IA solicitada pero no está disponible. Usando modo básico.")
            usar_ia = False
            
        if usar_ia and self.procesador_ia:
            return self.realizandoProcesoConIA(Textos)
        else:
            return self.realizandoProcesoBasico(Textos)
    
    def realizandoProcesoBasico(self,Textos):
        """Procesamiento básico original (sin IA)"""
        ContenedorTexto = Textos.replace(',', ', ')
        ContenedorTexto = ContenedorTexto.replace('\uf0fc ', '')
        ContenedorTexto = self.cambiandoBullets(ContenedorTexto)
        ContenedorTexto = self.colocandoPuntosDespuesRenglon(ContenedorTexto)
        ContenedorTexto = ' '.join(ContenedorTexto.split())
        ContenedorTexto = self.colocandoPuntosEnDondeNoLosHay(ContenedorTexto)
        ContenedorTexto = self.cambiandoBulletsdeCinco(ContenedorTexto)
        ContenedorTexto= ContenedorTexto.replace('\x0c', '\n ')
        ContenedorTexto = self.limpiarTextodeSaltoLinea(ContenedorTexto)
        ContenedorTexto = self.arreglandoNumros(ContenedorTexto)
        ContenedorTexto = self.arregloIncisos(ContenedorTexto)
        ContenedorTexto = self.insertarSaltosdeLineaEstrategicos(ContenedorTexto)
        ContenedorTexto = ContenedorTexto.lstrip()
        return ContenedorTexto
    
    def realizandoProcesoConIA(self, Textos):
        """
        Procesamiento híbrido: PRIMERO procesamiento básico completo, 
        DESPUÉS refinamiento con IA
        """
        try:
            self._notificar_progreso("Iniciando procesamiento híbrido...")
            
            # PASO 1: Ejecutar TODO el procesamiento básico original primero
            self._notificar_progreso("Aplicando procesamiento básico completo...")
            texto_procesado_basico = self.realizandoProcesoBasico(Textos)
            
            # PASO 2: Análisis del tipo de documento para la IA
            self._notificar_progreso("Analizando tipo de documento...")
            info_doc = self.procesador_ia.detectar_tipo_documento(texto_procesado_basico)
            tipo_detectado = info_doc.get('tipo', 'desconocido')
            
            # PASO 3: Refinamiento final con IA
            self._notificar_progreso(f"Refinando texto ({tipo_detectado})...")
            # Crear callback para el procesador IA
            def callback_ia(mensaje):
                self._notificar_progreso(mensaje)
            
            texto_final = self.procesador_ia.refinar_texto_procesado(
                texto_procesado_basico, 
                info_doc,
                callback=callback_ia
            )
            
            self._notificar_progreso("Procesamiento completado exitosamente")
            return texto_final
            
        except Exception as e:
            print(f"❌ Error en procesamiento IA: {e}")
            print("🔄 Fallback: devolviendo resultado de procesamiento básico...")
            return self.realizandoProcesoBasico(Textos)
    def cambiandoBullets(self,CambiandolosPuntos):
        CambiandolosPuntos = CambiandolosPuntos +"XXXX"
        Casilla4 = ""
        Casilla3 = ""
        Casilla2 = ""
        Casilla1 = ""
        TextoFinal =""
        for letra in CambiandolosPuntos:
            Final = Casilla4
            Casilla4 = Casilla3
            Casilla3 = Casilla2
            Casilla2 = Casilla1
            Casilla1 = letra
            if Casilla4 == "\n" and Casilla3 == "." and Casilla2 == " " and Casilla1.isupper():
                Casilla3 = Casilla3.replace('.', '•')
                TextoFinal = TextoFinal +Final
            elif Casilla4 == "\n" and Casilla3 == "o" and Casilla2 == " " and Casilla1.isupper():
                Casilla3 = Casilla3.replace('o', '•')
                TextoFinal = TextoFinal +Final
            elif Casilla4 == "\n" and Casilla3 == "-" and Casilla2 == " " and Casilla1.isupper():
                Casilla3 = Casilla3.replace('-', '•')
                TextoFinal = TextoFinal + Final
            elif Casilla4 == "\n" and Casilla3 == "*" and Casilla2 == " " and Casilla1.isupper():
                Casilla3 = Casilla3.replace('*', '•')
                TextoFinal = TextoFinal + Final
            elif Casilla4.islower() and Casilla3 == " " and Casilla2 == "\n" and Casilla1 == "\n":
                Casilla3 = Casilla3.replace(' ', '.\n')
                TextoFinal = TextoFinal + Final
            elif Casilla4.islower() and Casilla3 == "." and Casilla2.isupper() and Casilla1.islower():
                Casilla3 = ". "
                TextoFinal = TextoFinal + Final
            else:
                TextoFinal = TextoFinal + Final
        return TextoFinal
    def colocandoPuntosDespuesRenglon(self,ContenedorTexto):
        """
        Función desactivada permanentemente - problemas de puntuación incorrecta
        El refinamiento de puntuación se hace posteriormente con IA si está disponible
        """
        # Siempre devuelve el texto sin modificar
        # La IA se encargará del refinamiento al final del proceso
        return ContenedorTexto
    def colocandoPuntosEnDondeNoLosHay(self,ContenedorTexto):
        ContenedorTexto = ContenedorTexto +"XXXX"
        Casilla4 = ""
        Casilla3 = ""
        Casilla2 = ""
        Casilla1 = ""
        TextoFinal = ""
        for letra in ContenedorTexto:
            Final = Casilla4
            Casilla4 = Casilla3
            Casilla3 = Casilla2
            Casilla2 = Casilla1
            Casilla1 = letra
            if Casilla4.islower() and Casilla3 == "\n" and Casilla2.isupper() and Casilla1.islower():
                Casilla3 = Casilla3.replace('\n', '.')
                TextoFinal = TextoFinal + Final
            else:
                TextoFinal = TextoFinal + Final
        return TextoFinal
    def cambiandoBulletsdeCinco(self,CambiandolosPuntos):
        CambiandolosPuntos = CambiandolosPuntos +"xxxxx"
        Casilla5 = ""
        Casilla4 = ""
        Casilla3 = ""
        Casilla2 = ""
        Casilla1 = ""
        TextoFinal =""
        for letra in CambiandolosPuntos:
            Final = Casilla5
            Casilla5 = Casilla4
            Casilla4 = Casilla3
            Casilla3 = Casilla2
            Casilla2 = Casilla1
            Casilla1 = letra
            if Casilla5 == "\n" and Casilla4 == "." and Casilla3 == " " and Casilla2 == "\n" and Casilla1.isupper():
                Casilla4 = Casilla4.replace(".","•")
                TextoFinal = TextoFinal +Final
            elif Casilla5 == "\n" and Casilla4 == "o" and Casilla3 == " " and Casilla2 == "\n" and Casilla1.isupper():
                Casilla4 = Casilla4.replace("o","•")
                TextoFinal = TextoFinal +Final
            elif Casilla5 == "\n" and Casilla4 == "-" and Casilla3 == " " and Casilla2 == "\n" and Casilla1.isupper():
                Casilla4 = Casilla4.replace("-","•")
                TextoFinal = TextoFinal +Final
            elif Casilla5 == "\n" and Casilla4 == "*" and Casilla3 == " " and Casilla2 == "\n" and Casilla1.isupper():
                Casilla4 = Casilla4.replace("*","•")
                TextoFinal = TextoFinal +Final
            elif Casilla5.islower() and Casilla4 == " " and Casilla3 == "\n " and Casilla2 == "\n" and Casilla1.isupper():
                Casilla4 = ".\n"
                TextoFinal = TextoFinal +Final
            else:
                TextoFinal = TextoFinal +Final
        return TextoFinal
    def limpiarTextodeSaltoLinea(self,TextoaLimpiar):
        TextoLimpio = ""
        for linea in TextoaLimpiar:
            if linea[-1:]=='\n':
                linea=linea[:-1]
            TextoLimpio = TextoLimpio + linea
        return TextoLimpio
    def arreglandoNumros(self,CambiandolosPuntos):
        CambiandolosPuntos = CambiandolosPuntos +"xxxx"
        Casilla4 = ""
        Casilla3 = ""
        Casilla2 = ""
        Casilla1 = ""
        TextoFinal = ""
        for letra in CambiandolosPuntos:
            Final = Casilla4
            Casilla4 = Casilla3
            Casilla3 = Casilla2
            Casilla2 = Casilla1
            Casilla1 = letra
            if Casilla4.isnumeric() and Casilla3 == "." and Casilla2 == "\n" and Casilla1 == "\n":
                Casilla3 = Casilla3.replace('.', '.')
                TextoFinal = TextoFinal +Final
            elif Casilla4.isnumeric() and Casilla3 == "." and Casilla2 == " " and Casilla1.isupper():
                Casilla3 = Casilla3.replace('.', '.')
                TextoFinal = TextoFinal + Final
            else:
                TextoFinal = TextoFinal + Final
        return TextoFinal
    def arregloIncisos(self,texto):
        texto=texto + "XXXXXX"
        Casilla6 = " "
        Casilla5 = " "
        Casilla4 = " "
        Casilla3 = " "
        Casilla2 = " "
        Casilla1 = " "
        Final = " "
        TextoFinal = ""
        for letra in texto:
            Final = Casilla6
            Casilla6 = Casilla5
            Casilla5 = Casilla4
            Casilla4 = Casilla3
            Casilla3 = Casilla2
            Casilla2 = Casilla1
            Casilla1 = letra
            verificar = Casilla6+Casilla5+Casilla4
            DatoaVerificar = re.compile(r'\.\d\.')
            comprobar = DatoaVerificar.search(verificar)
            if comprobar != None and Casilla3 == "\n" and Casilla2 == "\n" and Casilla1.isupper():
                Casilla3 = " "
                Casilla2 = " "
                TextoFinal = TextoFinal +Final
            else:
                TextoFinal = TextoFinal +Final
        return TextoFinal
    def insertarSaltosdeLineaEstrategicos(self,RegresoLimpiarTexto):
        ContenedorTexto = RegresoLimpiarTexto
        ContenedorTexto = ContenedorTexto.replace("•","\n•")
        ContenedorTexto = ContenedorTexto.replace("-\n","")
        ContenedorTexto = ContenedorTexto.replace("- \n","")
        ContenedorTexto = ContenedorTexto.replace("- ","")
        ContenedorTexto = ContenedorTexto.replace('.)', ').')
        ContenedorTexto = ContenedorTexto.replace('."', '".')
        ContenedorTexto = ContenedorTexto.replace('!', '!\n')
        ContenedorTexto = ContenedorTexto.replace('¿','\n¿')
        ContenedorTexto = ContenedorTexto.replace('?', '?\n')
        ContenedorTexto = ContenedorTexto.replace(':', ':\n')
        ContenedorTexto = ContenedorTexto.replace('y/o', 'y, o')
        ContenedorTexto = ContenedorTexto.replace('y / o', 'y, o')
        ContenedorTexto = ContenedorTexto.replace('(', '( ')
        ContenedorTexto = ContenedorTexto.replace(')', ' )')
        ContenedorTexto = ContenedorTexto.replace('}', '}\n')
        ContenedorTexto = ContenedorTexto.replace('. .', '.')
        ContenedorTexto = ContenedorTexto.replace('.', '.\n')
        ContenedorTexto = ContenedorTexto.replace('\npng', 'png')
        ContenedorTexto = ContenedorTexto.replace('\njpg', 'jpg')
        ContenedorTexto = ContenedorTexto.replace('\npdf', 'pdf')
        ContenedorTexto = ContenedorTexto.replace('\n.\n', '\n')
        return ContenedorTexto
    
    def _dividir_en_palabras(self, texto):
        """Divide el texto en palabras preservando espacios y puntuación"""
        # Usar regex para dividir manteniendo los separadores
        import re
        # Patrón que captura palabras y espacios/puntuación
        patron = r'(\w+|[^\w\s]|\s+)'
        palabras = re.findall(patron, texto)
        return palabras
    
    def _resaltar_palabra(self, inicio, fin):
        """Resalta una palabra en el widget de texto"""
        if not self.texto_widget:
            return
        
        try:
            # Limpiar resaltados anteriores
            self.texto_widget.tag_remove("highlight", "1.0", "end")
            
            # Aplicar nuevo resaltado
            self.texto_widget.tag_add("highlight", inicio, fin)
            self.texto_widget.tag_config("highlight", 
                                        background="#ffff00",  # Amarillo
                                        foreground="#000000",  # Negro
                                        font=("Arial", 10, "bold"))
            
            # Scroll automático para mantener la palabra visible
            self.texto_widget.see(inicio)
        except Exception as e:
            pass  # Si hay error, continuar sin resaltado
    
    def _limpiar_resaltado(self):
        """Limpia todos los resaltados del texto"""
        if self.texto_widget:
            try:
                self.texto_widget.tag_remove("highlight", "1.0", "end")
            except:
                pass
    
    def _leer_con_resaltado_pyttsx3(self, texto):
        """Lee texto con pyttsx3 y resalta palabras en tiempo real - SINCRONIZACIÓN MEJORADA CON PAUSAS"""
        try:
            print("🎙️ Usando pyttsx3 (offline, voces del sistema)...")
            engine = pyttsx3.init()
            
            # Configurar voz
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'spanish' in voice.name.lower() or 'español' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    print(f"✅ Voz español detectada: {voice.name}")
                    break
            
            # Configurar velocidad y volumen
            velocidad = engine.getProperty('rate')
            engine.setProperty('rate', 125)
            engine.setProperty('volume', 0.9)
            
            if not self.texto_widget:
                # Si no hay widget, solo reproducir
                engine.say(texto)
                engine.runAndWait()
                return True
            
            # Obtener contenido completo del widget
            contenido_completo = self.texto_widget.get("1.0", "end-1c")
            
            # Dividir en palabras y extraer información de contexto
            import re
            palabras_info = []
            
            # Patrón para capturar palabras y el contexto después de ellas
            for match in re.finditer(r'(\w+)([\s\.,;:!?\n]*)', contenido_completo):
                palabra = match.group(1)
                contexto_despues = match.group(2)
                inicio_idx = match.start(1)
                
                # Calcular posición en formato Tkinter
                lineas_antes = contenido_completo[:inicio_idx].count('\n')
                col = inicio_idx - contenido_completo.rfind('\n', 0, inicio_idx) - 1
                
                inicio_pos = f"{lineas_antes + 1}.{col}"
                fin_pos = f"{lineas_antes + 1}.{col + len(palabra)}"
                
                # Determinar tipo de pausa después de la palabra
                pausa_extra = 0
                if '\n' in contexto_despues:
                    # Salto de línea = pausa larga
                    pausa_extra = PAUSA_SALTO_LINEA
                elif '.' in contexto_despues or '!' in contexto_despues or '?' in contexto_despues:
                    # Punto, exclamación, interrogación = pausa media
                    pausa_extra = PAUSA_PUNTO
                elif ',' in contexto_despues or ';' in contexto_despues or ':' in contexto_despues:
                    # Coma, punto y coma, dos puntos = pausa corta
                    pausa_extra = PAUSA_COMA
                
                palabras_info.append({
                    'palabra': palabra,
                    'inicio': inicio_pos,
                    'fin': fin_pos,
                    'pausa_extra': pausa_extra
                })
            
            if not palabras_info:
                engine.say(texto)
                engine.runAndWait()
                return True
            
            # Calcular duración base por palabra
            velocidad_wpm = engine.getProperty('rate')
            duracion_base = 60.0 / velocidad_wpm if velocidad_wpm > 0 else 0.48
            
            # Calcular duración total para cada palabra (palabra + pausa)
            duraciones = []
            for info in palabras_info:
                palabra = info['palabra']
                
                # Factor de longitud de palabra
                factor_longitud = 1.0 + (len(palabra) - UMBRAL_PALABRA_LARGA) * FACTOR_LONGITUD_PALABRA \
                                 if len(palabra) > UMBRAL_PALABRA_LARGA else 1.0
                
                # Duración de la palabra
                duracion_palabra = duracion_base * factor_longitud
                
                # Duración total = palabra + pausa de puntuación
                duracion_total = duracion_palabra + info['pausa_extra']
                
                duraciones.append(duracion_total)
            
            # Iniciar thread para resaltado sincronizado
            def resaltar_sincronizado():
                # Delay inicial más ajustado
                time.sleep(DELAY_INICIAL + 0.1)
                
                for i, info in enumerate(palabras_info):
                    if not self.resaltado_activo:
                        break
                    
                    # Resaltar palabra actual
                    if self.texto_widget:
                        try:
                            inicio = info['inicio']
                            fin = info['fin']
                            self.texto_widget.after(0, lambda i=inicio, f=fin: self._resaltar_palabra(i, f))
                        except:
                            pass
                    
                    # Esperar la duración calculada (palabra + pausa)
                    if i < len(duraciones):
                        time.sleep(duraciones[i])
                
                # Pausa adicional al final antes de limpiar
                time.sleep(0.5)
                
                # Limpiar resaltado al final
                if self.texto_widget:
                    self.texto_widget.after(0, self._limpiar_resaltado)
            
            self.resaltado_activo = True
            self.hilo_lectura = threading.Thread(target=resaltar_sincronizado, daemon=True)
            self.hilo_lectura.start()
            
            # Reproducir el texto
            engine.say(texto)
            engine.runAndWait()
            
            # Esperar usando delay configurable más tiempo para que termine el resaltado
            time.sleep(DELAY_LIMPIEZA + 0.3)
            self.resaltado_activo = False
            
            print("✅ Texto reproducido con pyttsx3")
            return True
            
        except Exception as e:
            self.resaltado_activo = False
            print(f"❌ Error con pyttsx3: {e}")
            return False
    
    def leerArchivo(self, archivo):
        """
        Sintetiza voz del texto usando TTS offline/online según disponibilidad.
        Prioridad: 1) Piper (offline alta calidad), 2) pyttsx3 (offline básico), 3) gTTS (online)
        INCLUYE RESALTADO DE PALABRAS EN TIEMPO REAL
        """
        if not archivo or archivo.strip() == "":
            print("⚠️ No hay texto para leer")
            return
        
        texto = archivo.strip()
        exito = False
        
        # Limitar longitud para evitar tiempos muy largos
        if len(texto) > 5000:
            print("⚠️ Texto muy largo, solo se leerán los primeros 5000 caracteres")
            texto = texto[:5000]
        
        # Detener cualquier lectura anterior
        self.resaltado_activo = False
        self._limpiar_resaltado()
        
        # Método 1: Piper TTS (offline, alta calidad) - SI ESTÁ DISPONIBLE
        # Nota: Piper genera archivo de audio, más difícil sincronizar resaltado
        # Por ahora, no resaltamos con Piper
        if self.piper_path and self.piper_model and not exito:
            try:
                print("🎙️ Usando Piper TTS (offline, alta calidad)...")
                print("   ℹ️  Resaltado no disponible con Piper (genera archivo de audio)")
                output_file = "text_to_read_piper.wav"
                
                # Ejecutar Piper
                cmd = [
                    self.piper_path,
                    "--model", self.piper_model,
                    "--output_file", output_file
                ]
                
                process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate(input=texto, timeout=30)
                
                if process.returncode == 0 and os.path.exists(output_file):
                    # Reproducir el archivo generado
                    os.startfile(output_file)
                    exito = True
                    print("✅ Audio generado con Piper TTS")
                else:
                    print(f"⚠️ Piper falló: {stderr[:100]}")
            except Exception as e:
                print(f"⚠️ Error con Piper TTS: {str(e)[:100]}")
        
        # Método 2: pyttsx3 (offline, voces del sistema) - PREDETERMINADO CON RESALTADO
        if not exito:
            exito = self._leer_con_resaltado_pyttsx3(texto)
        
        # Método 3: gTTS (online) - SOLO COMO FALLBACK (sin resaltado)
        if not exito and GTTS_DISPONIBLE:
            try:
                print("🌐 Intentando gTTS (requiere conexión a Internet)...")
                print("   ℹ️  Resaltado no disponible con gTTS (genera archivo de audio)")
                speech = gTTS(text=texto, lang='es', slow=False)
                output_file = "text_to_read.mp3"
                speech.save(output_file)
                
                # Reproducir el archivo
                os.startfile(output_file)
                exito = True
                print("✅ Audio generado con gTTS (online)")
            except Exception as e:
                print(f"❌ Error con gTTS (sin conexión?): {e}")
        
        if not exito:
            print("❌ No se pudo reproducir el texto. Verifica que al menos pyttsx3 esté instalado.")
    
    def detener_lectura(self):
        """Detiene la lectura actual y limpia el resaltado"""
        self.resaltado_activo = False
        self._limpiar_resaltado()
        print("🛑 Lectura detenida")
    
    def cambiar_motor_tts(self, motor):
        """Permite cambiar el motor TTS preferido ('pyttsx3', 'piper', 'gtts')"""
        motores_validos = ['pyttsx3', 'piper', 'gtts']
        if motor.lower() in motores_validos:
            self.motor_tts = motor.lower()
            print(f"✅ Motor TTS cambiado a: {motor}")
            return True
        else:
            print(f"❌ Motor '{motor}' no válido. Opciones: {motores_validos}")
            return False

