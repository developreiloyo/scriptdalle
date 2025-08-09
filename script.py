import requests
import json
import os
from datetime import datetime
import base64

class OpenAIImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/images/generations"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_image(self, prompt, model="dall-e-3", size="1024x1024", quality="standard", n=1):
        """
        Genera una imagen usando la API de OpenAI
        
        Args:
            prompt (str): Descripción de la imagen a generar
            model (str): Modelo a usar ("dall-e-2" o "dall-e-3")
            size (str): Tamaño de la imagen ("256x256", "512x512", "1024x1024", "1024x1792", "1792x1024")
            quality (str): Calidad de la imagen ("standard" o "hd") - solo para dall-e-3
            n (int): Número de imágenes a generar (1-10 para dall-e-2, solo 1 para dall-e-3)
        
        Returns:
            dict: Respuesta de la API
        """
        
        payload = {
            "model": model,
            "prompt": prompt,
            "n": n,
            "size": size
        }
        
        # Agregar calidad solo para dall-e-3
        if model == "dall-e-3":
            payload["quality"] = quality
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            return None
    
    def download_image(self, image_url, filename=None, download_folder="images"):
        """
        Descarga una imagen desde una URL
        
        Args:
            image_url (str): URL de la imagen
            filename (str): Nombre del archivo (opcional)
            download_folder (str): Carpeta donde descargar (por defecto: "images")
        
        Returns:
            str: Ruta del archivo descargado
        """
        try:
            # Crear carpeta si no existe
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
                print(f"Carpeta creada: {download_folder}")
            
            response = requests.get(image_url)
            response.raise_for_status()
            
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_image_{timestamp}.png"
            
            # Ruta completa del archivo
            filepath = os.path.join(download_folder, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"Imagen descargada: {filepath}")
            return filepath
        
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar la imagen: {e}")
            return None
    
    def generate_and_download(self, prompt, model="dall-e-3", size="1024x1024", quality="standard", download=True, download_folder="images"):
        """
        Genera y descarga una imagen
        
        Args:
            prompt (str): Descripción de la imagen
            model (str): Modelo a usar
            size (str): Tamaño de la imagen
            quality (str): Calidad de la imagen
            download (bool): Si descargar la imagen automáticamente
            download_folder (str): Carpeta donde descargar
        
        Returns:
            dict: Información de la imagen generada
        """
        print(f"Generando imagen con prompt: {prompt[:50]}...")
        
        result = self.generate_image(prompt, model, size, quality)
        
        if result and 'data' in result:
            image_info = result['data'][0]
            image_url = image_info['url']
            
            print(f"Imagen generada exitosamente!")
            print(f"URL: {image_url}")
            
            if download:
                filename = self.download_image(image_url, download_folder=download_folder)
                image_info['local_file'] = filename
            
            return image_info
        else:
            print("Error al generar la imagen")
            return None

def main():
    # Tu API key
    API_KEY = "tu_api_key_aqui"  # Reemplaza con tu clave de API de OpenAI
    
    # Tu prompt
    PROMPT = """A modern digital collage illustrating the concept of digital consumption. In the center, a large clock with faint digital circuits inside, symbolizing time and technology. Overlaid on the clock is a glowing fingerprint, representing identity and personal data. Around the clock, floating icons of popular apps (social media, streaming, e-commerce, messaging) are arranged in a circular collage — icons like Instagram, YouTube, Amazon, WhatsApp, Spotify, etc., subtly glowing and interconnected by thin light lines. The background is abstract, with soft gradients of blue, purple, and gray, evoking a digital atmosphere. At the top, bold clean text reads: 'Consumo digital: qué cambia y por qué importa'. At the bottom, a key message in slightly smaller font: 'El consumo digital reconfigura atención, decisiones y vínculos'. The overall style is minimalist, futuristic, and conceptual — suitable for an educational or documentary opening scene. High resolution, 16:9 aspect ratio."""
    
    # Crear el generador
    generator = OpenAIImageGenerator(API_KEY)
    
    # Generar imagen con aspect ratio 16:9 (1792x1024)
    image_info = generator.generate_and_download(
        prompt=PROMPT,
        model="dall-e-3",
        size="1792x1024",  # 16:9 aspect ratio
        quality="hd",      # Alta calidad
        download=True,
        download_folder="imagenes_generadas"  # Carpeta personalizada
    )
    
    if image_info:
        print("\n✅ Imagen generada exitosamente!")
        print(f"Archivo local: {image_info.get('local_file', 'No descargado')}")
        print(f"URL original: {image_info['url']}")
        
        # Si quieres ver información adicional de DALL-E-3
        if 'revised_prompt' in image_info:
            print(f"\nPrompt revisado por DALL-E-3:")
            print(image_info['revised_prompt'])
    else:
        print("❌ Error al generar la imagen")

if __name__ == "__main__":
    main()