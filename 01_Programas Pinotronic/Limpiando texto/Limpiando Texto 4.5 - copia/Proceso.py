import re
import pyttsx3
from gtts import gTTS

class Operativo:
    def __init__(self):
        pass
    def sustitucionTexto(self,textoOriginal,texto1,texto2):
        return textoOriginal.replace(texto1, texto2)
    def realizandoProceso(self,Textos):
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
        # Función desactivada - ya no coloca puntos delante de letras mayúsculas
        # Simplemente devuelve el texto sin modificaciones
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
