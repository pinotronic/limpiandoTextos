import re
import pyttsx3
from gtts import gTTS
try:
    from ProcesadorIA import ProcesadorDeepSeek
    from config_ia import DEEPSEEK_API_KEY, IA_CONFIG
    IA_DISPONIBLE = True
except ImportError:
    IA_DISPONIBLE = False
    print("Módulos de IA no disponibles. Funcionando en modo básico.")

class Operativo:
    def __init__(self):
        self.ia_habilitada = False
        self.procesador_ia = None
        
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
        """Procesamiento mejorado con IA de DeepSeek"""
        try:
            print("🧠 Procesando con IA DeepSeek...")
            
            # Análisis preliminar del documento
            info_doc = self.procesador_ia.detectar_tipo_documento(Textos)
            print(f"📄 Tipo de documento detectado: {info_doc.get('tipo', 'desconocido')}")
            
            # Procesamiento básico inicial (limpieza simple)
            ContenedorTexto = Textos.replace(',', ', ')
            ContenedorTexto = ContenedorTexto.replace('\uf0fc ', '')
            ContenedorTexto = self.cambiandoBullets(ContenedorTexto)
            # Saltamos las funciones problemáticas y usamos IA en su lugar
            ContenedorTexto = ' '.join(ContenedorTexto.split())
            ContenedorTexto = self.cambiandoBulletsdeCinco(ContenedorTexto)
            ContenedorTexto= ContenedorTexto.replace('\x0c', '\n ')
            ContenedorTexto = self.limpiarTextodeSaltoLinea(ContenedorTexto)
            
            # Aquí es donde la IA hace la magia - reemplaza las funciones problemáticas
            ContenedorTexto = self.procesador_ia.corregir_puntuacion_inteligente(ContenedorTexto)
            
            # Continuamos con el procesamiento básico final
            ContenedorTexto = self.arreglandoNumros(ContenedorTexto)
            ContenedorTexto = self.arregloIncisos(ContenedorTexto)
            
            # Procesamiento final con IA para optimizar
            ContenedorTexto = self.procesador_ia.limpiar_texto_inteligente(ContenedorTexto)
            
            ContenedorTexto = ContenedorTexto.lstrip()
            print("✅ Procesamiento con IA completado")
            return ContenedorTexto
            
        except Exception as e:
            print(f"❌ Error en procesamiento IA: {e}")
            print("🔄 Fallback a procesamiento básico...")
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
        Función mejorada - usa IA cuando está disponible, 
        de lo contrario mantiene texto sin modificaciones
        """
        if self.ia_habilitada and self.procesador_ia:
            # Usar IA para corrección inteligente de puntuación
            return self.procesador_ia.corregir_puntuacion_inteligente(ContenedorTexto)
        else:
            # Modo básico - no hace cambios para evitar errores
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
    def leerArchivo(self,archivo):
        speech = gTTS(text=archivo, lang='es')
        speech.save("text_to_read.mp3")
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 125)
        engine.say(archivo)
        engine.runAndWait()
