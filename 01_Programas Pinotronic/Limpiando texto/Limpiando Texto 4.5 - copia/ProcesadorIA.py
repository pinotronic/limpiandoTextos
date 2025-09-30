"""
Módulo de Inteligencia Artificial para Limpiando Texto
Utiliza DeepSeek API para procesamiento inteligente de texto
"""

import requests
import json
import time
from typing import Optional, Dict, Any

class ProcesadorDeepSeek:
    def __init__(self, api_key: str):
        """
        Inicializa el procesador con la API key de DeepSeek
        
        Args:
            api_key (str): Tu API key de DeepSeek
        """
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
    def _llamar_api(self, prompt: str, max_tokens: int = 2000) -> Optional[str]:
        """
        Realiza llamada a la API de DeepSeek
        
        Args:
            prompt (str): El prompt para enviar a la API
            max_tokens (int): Máximo número de tokens en la respuesta
            
        Returns:
            str: Respuesta de la API o None en caso de error
        """
        try:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": """Eres un experto en procesamiento de texto OCR y limpieza de documentos. 
                        Tu trabajo es mejorar texto extraído de documentos escaneados manteniendo:
                        1. El significado original
                        2. El formato apropiado
                        3. La estructura del documento
                        
                        REGLAS IMPORTANTES:
                        - NO agregues puntos antes de títulos, encabezados o nombres propios
                        - SÍ corrige errores evidentes de OCR
                        - Mantén las listas y viñetas en su formato original
                        - Preserva saltos de línea importantes para la estructura
                        """
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.1,  # Baja temperatura para respuestas más consistentes
                "stream": False
            }
            
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"Error en API DeepSeek: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error al llamar a DeepSeek: {str(e)}")
            return None
    
    def limpiar_texto_inteligente(self, texto: str) -> str:
        """
        Limpia texto usando IA de DeepSeek de manera inteligente
        
        Args:
            texto (str): Texto a limpiar
            
        Returns:
            str: Texto limpiado o texto original si hay error
        """
        if not texto or len(texto.strip()) == 0:
            return texto
            
        # Dividir texto largo en chunks para evitar límites de tokens
        max_chunk_size = 3000
        if len(texto) > max_chunk_size:
            return self._procesar_texto_largo(texto)
        
        prompt = f"""
        Limpia y mejora este texto que proviene de OCR. Corrige errores obvios pero mantén la estructura original:

        TEXTO A LIMPIAR:
        {texto}

        INSTRUCCIONES:
        1. Corrige errores de OCR (caracteres mal reconocidos)
        2. Ajusta espaciado y puntuación donde sea necesario
        3. NO agregues puntos antes de títulos o nombres propios
        4. Mantén saltos de línea importantes
        5. Preserva listas y viñetas
        6. Devuelve SOLO el texto corregido, sin explicaciones adicionales
        """
        
        resultado = self._llamar_api(prompt)
        return resultado if resultado else texto
    
    def _procesar_texto_largo(self, texto: str) -> str:
        """
        Procesa texto largo dividiéndolo en chunks
        
        Args:
            texto (str): Texto largo a procesar
            
        Returns:
            str: Texto procesado completo
        """
        # Dividir por párrafos para mantener contexto
        parrafos = texto.split('\n\n')
        resultado_chunks = []
        chunk_actual = ""
        
        for parrafo in parrafos:
            if len(chunk_actual + parrafo) > 2500:  # Dejar margen para el prompt
                if chunk_actual:
                    # Procesar chunk actual
                    chunk_procesado = self.limpiar_texto_inteligente(chunk_actual)
                    resultado_chunks.append(chunk_procesado)
                    chunk_actual = parrafo
                else:
                    # Párrafo muy largo, procesarlo solo
                    chunk_procesado = self.limpiar_texto_inteligente(parrafo)
                    resultado_chunks.append(chunk_procesado)
            else:
                chunk_actual += "\n\n" + parrafo if chunk_actual else parrafo
        
        # Procesar último chunk
        if chunk_actual:
            chunk_procesado = self.limpiar_texto_inteligente(chunk_actual)
            resultado_chunks.append(chunk_procesado)
        
        return "\n\n".join(resultado_chunks)
    
    def detectar_tipo_documento(self, texto: str) -> Dict[str, Any]:
        """
        Analiza el tipo de documento para ajustar el procesamiento
        
        Args:
            texto (str): Texto a analizar
            
        Returns:
            dict: Información sobre el tipo de documento
        """
        prompt = f"""
        Analiza este texto y determina qué tipo de documento es. Responde en formato JSON:

        TEXTO:
        {texto[:1000]}...

        Responde con este formato JSON exacto:
        {{
            "tipo": "articulo|legal|lista|email|academico|tecnico|otro",
            "estructura": "formal|informal|lista|tabla",
            "idioma": "es|en|otro",
            "tiene_titulos": true|false,
            "tiene_listas": true|false,
            "nivel_errores_ocr": "bajo|medio|alto"
        }}
        """
        
        resultado = self._llamar_api(prompt, max_tokens=200)
        
        try:
            return json.loads(resultado) if resultado else {
                "tipo": "otro",
                "estructura": "informal",
                "idioma": "es",
                "tiene_titulos": False,
                "tiene_listas": False,
                "nivel_errores_ocr": "medio"
            }
        except:
            return {
                "tipo": "otro",
                "estructura": "informal", 
                "idioma": "es",
                "tiene_titulos": False,
                "tiene_listas": False,
                "nivel_errores_ocr": "medio"
            }
    
    def corregir_puntuacion_inteligente(self, texto: str) -> str:
        """
        Reemplaza la función problemática con IA inteligente
        
        Args:
            texto (str): Texto con posibles problemas de puntuación
            
        Returns:
            str: Texto con puntuación corregida
        """
        if not texto or len(texto.strip()) == 0:
            return texto
            
        prompt = f"""
        Corrige ÚNICAMENTE la puntuación de este texto. NO cambies palabras, solo ajusta puntos, comas y espacios:

        REGLAS ESPECÍFICAS:
        1. NO agregues puntos antes de títulos (texto en mayúsculas al inicio de línea)
        2. NO agregues puntos antes de nombres propios
        3. NO agregues puntos antes de elementos de lista
        4. SÍ agrega puntos al final de oraciones completas que no los tengan
        5. Mantén la estructura original de saltos de línea

        TEXTO:
        {texto}

        Devuelve SOLO el texto con puntuación corregida:
        """
        
        resultado = self._llamar_api(prompt)
        return resultado if resultado else texto
    
    def validar_api_key(self) -> bool:
        """
        Valida que la API key funcione correctamente
        
        Returns:
            bool: True si la API key es válida
        """
        test_prompt = "Responde solo con 'OK'"
        resultado = self._llamar_api(test_prompt, max_tokens=10)
        return resultado is not None and "OK" in resultado