from fastapi import FastAPI
from pydantic import BaseModel
import cohere
import os
import pymysql
from dotenv import load_dotenv
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

# Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Inicializar FastAPI
app = FastAPI()



# Montar archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# Modelo para el teorema
class Teorema(BaseModel):
    teorema: str
    
@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/add_theorem")
async def add_theorem(teorem: Teorema):
    # Inicializar cliente Cohere con la API Key
    co = cohere.Client(api_key=API_KEY)

    # Realizar la llamada a Cohere para obtener la explicación, conocimientos previos y ejemplo
    prompt = f"""
    Eres un profesor de matemáticas que explica teoremas de una manera sencilla.
    Tu objetivo es proporcionar tres respuestas de manera clara:
    1. Explicación: Explica de forma sencilla el teorema proporcionado.
    2. Conocimientos Previos: Qué conocimientos debería tener un estudiante para entender este teorema.
    3. Ejemplo: Da un ejemplo sencillo de cómo aplicar este teorema.
    
    Por favor, marca claramente el inicio de cada sección con los títulos respectivos: 'Explicación:', 'Conocimientos Previos:', 'Ejemplo:'.
    
    Teorema: {teorem.teorema}
    """

    # Llamada a la API de Cohere para generar la respuesta
    response = co.generate(
        model="command-r-plus-08-2024",  # Verifica si este es el modelo correcto
        prompt=prompt,
        max_tokens=500
    )

    # Procesar la respuesta y extraer las tres partes
    if response and response.generations:
        text = response.generations[0].text.strip()

        # Definir las secciones que buscamos
        explicacion = ""
        conocimientos_previos = ""
        ejemplo = ""

        # Usamos los títulos de las secciones para extraer cada parte
        if 'Explicación:' in text:
            explicacion = text.split('Explicación:')[1].split('Conocimientos Previos:')[0].strip()
        if 'Conocimientos Previos:' in text:
            conocimientos_previos = text.split('Conocimientos Previos:')[1].split('Ejemplo:')[0].strip()
        if 'Ejemplo:' in text:
            ejemplo = text.split('Ejemplo:')[1].strip()

        # Si alguna sección no está presente, asignar un mensaje por defecto
        if not explicacion:
            explicacion = "Explicación no generada."
        if not conocimientos_previos:
            conocimientos_previos = "Conocimientos previos no generados."
        if not ejemplo:
            ejemplo = "Ejemplo no generado."

        # Convertir los saltos de línea para el formato HTML
        explicacion = explicacion.replace('\n', '<br>')
        conocimientos_previos = conocimientos_previos.replace('\n', '<br>')
        ejemplo = ejemplo.replace('\n', '<br>')

    else:
        explicacion = "Explicación no generada."
        conocimientos_previos = "Conocimientos previos no generados."
        ejemplo = "Ejemplo no generado."

    # Insertar el teorema y las respuestas en la base de datos
    db = pymysql.connect(host =DB_HOST  ,
                     user = DB_USER,
                     password = DB_PASSWORD,
                     cursorclass = pymysql.cursors.DictCursor
            )

    cursor = db.cursor()

    # Usar la base de datos
    cursor.execute("USE math_database")
    
    # Insertar el teorema en la base de datos
    query = """INSERT INTO theorem (teorema, explicacion, conocimientos_previos, ejemplo) 
               VALUES (%s, %s, %s, %s)"""
    
    # Insertar los datos en la base de datos
    cursor.execute(query, (teorem.teorema, explicacion, conocimientos_previos, ejemplo))
    db.commit()
    db.close()
    cursor.close()

    # Retornar las respuestas como un JSON
    return {
        "teorema": teorem.teorema,
        "explicacion": explicacion,
        "conocimientos_previos": conocimientos_previos,
        "ejemplo": ejemplo
    }


# Arrancar el servidor
if __name__ == "__main__":
    uvicorn.run("modelo_app_html:app", host="0.0.0.0", port=8000, reload=True)
