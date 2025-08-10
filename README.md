# 🖼️ Generador y Descargador de Imágenes con DALL·E (OpenAI)

Script en Python que genera y descarga imágenes usando la API de OpenAI (modelos DALL·E 2/3). Incluye una clase lista para reutilizar en otros proyectos y un main() de ejemplo que guarda la imagen localmente.

    ⚠️ Seguridad: No publiques tu API key en el repositorio ni la dejes hardcodeada en el código. Usa variables de entorno.

## 🚀 Características

    Generación de imágenes con dall-e-3 (y dall-e-2 si lo necesitas).

    Control de tamaño (256x256, 512x512, 1024x1024, 1024x1792, 1792x1024).

    Control de calidad (standard o hd, solo para dall-e-3).

    Descarga automática en una carpeta configurable.

    Manejo básico de errores y mensajes de estado.

    Devuelve la URL y, cuando aplique, el revised_prompt de DALL·E 3.

## 📦 Requisitos

    Python 3.9+

    Dependencias:

    pip install requests

## 🔧 Configuración de la API Key
Opción A) Variable de entorno (recomendada)

    Exporta tu key (Linux/macOS):

export OPENAI_API_KEY="tu_api_key"

Windows (PowerShell):

setx OPENAI_API_KEY "tu_api_key"

En el código, reemplaza la linea del API_KEY por:

    API_KEY = os.getenv("OPENAI_API_KEY")

Opción B) Archivo .env (opcional)

    Crea .env con:

    OPENAI_API_KEY=tu_api_key

    Cárgalo en tu script (por ejemplo, con python-dotenv).

    Añade .env a tu .gitignore:

    .env

## 🗂️ Estructura sugerida

tu-proyecto/
├─ dalle_downloader.py      # (este script)
├─ imagenes_generadas/      # (se crea automáticamente)
└─ README.md

## ▶️ Uso rápido

    Guarda el código como dalle_downloader.py (o el nombre que prefieras).

    Instala dependencias y configura tu API key (ver arriba).

    Ejecuta:

python dalle_downloader.py

El ejemplo del main():

    usa dall-e-3

    tamaño 16:9 (1792x1024)

    calidad hd

    guarda la imagen en imagenes_generadas/

Verás en consola la ruta local y la URL de la imagen.
🧩 API y parámetros (clase OpenAIImageGenerator)

generate_image(prompt, model="dall-e-3", size="1024x1024", quality="standard", n=1)

    prompt (str, requerido): descripción de la imagen.

    model (str): "dall-e-3" (recomendado) o "dall-e-2".

    size (str): "256x256", "512x512", "1024x1024", "1024x1792", "1792x1024".

    quality (str): "standard" o "hd" (solo dall-e-3).

    n (int): cantidad de imágenes (en dall-e-3 es 1; dall-e-2 permite 1–10).

download_image(image_url, filename=None, download_folder="images")

    Descarga la URL en download_folder (crea la carpeta si no existe).

    Si filename es None, genera uno con timestamp.

generate_and_download(prompt, model="dall-e-3", size="1024x1024", quality="standard", download=True, download_folder="images")

    Orquesta generación y descarga.

    Devuelve un dict con info de la imagen (url, revised_prompt si aplica y local_file si se descargó).

📝 Ejemplo mínimo (como librería)

from dalle_downloader import OpenAIImageGenerator
import os

gen = OpenAIImageGenerator(api_key=os.getenv("OPENAI_API_KEY"))
info = gen.generate_and_download(
    prompt="A minimalist poster of a hummingbird made of geometric shapes",
    model="dall-e-3",
    size="1024x1024",
    quality="standard",
    download=True,
    download_folder="output"
)
print(info)

## 🛠️ Solución de problemas

    401 Unauthorized: revisa tu API key o variable de entorno.

    429 Rate limit: demasiadas solicitudes; espera y reintenta.

    400 Bad Request: modelo o tamaño inválidos; valida parámetros.

    403/Insufficient Quota: revisa facturación/saldo en tu cuenta de OpenAI.

    Conexión/timeout: verifica tu red y reinténtalo.

## 📌 Notas y buenas prácticas

    No hardcodees tu API key en el código (ni la subas a Git).

    dall-e-3 ignora n>1; si necesitas múltiples variaciones, llama varias veces.

    Los tamaños panorámicos: 1792x1024 (16:9) y vertical: 1024x1792.

    El campo revised_prompt puede venir en la respuesta de dall-e-3 y es útil para auditoría.

    El módulo base64 está importado pero no se usa en este script (queda como mejora si decides pedir la imagen como b64_json).

## 🧭 Roadmap (mejoras sugeridas)

    Soporte para response_format="b64_json" y guardado desde base64.

    Reintentos con exponential backoff.

    CLI con argumentos (argparse).

    Tests y tipado con mypy.

    Logging estructurado.

📄 Licencia

## MIT. Usa y adapta libremente, manteniendo el aviso de licencia.
⚖️ Aviso

Generar imágenes consume crédito en tu cuenta de OpenAI. Revisa precios y límites en la consola de OpenAI. Asegúrate de cumplir con las políticas de uso y derechos del contenido generado.
