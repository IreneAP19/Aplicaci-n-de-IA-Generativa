from fastapi import FastAPI
from pydantic import BaseModel
import cohere
import os
import pymysql
from dotenv import load_dotenv
import uvicorn
from flask import Flask, render_template, request, jsonify
import requests

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Initialize FastAPI
app = FastAPI()


class Teorema(BaseModel):
    teorema: str

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Endpoint to add a new theorem to the database
@app.post("/add_theorem")
async def add_theorem(theorem: Teorema):
    # Get explanation and required knowledge from Cohere
    # Initialize Cohere API client
    co = cohere.ClientV2(api_key=API_KEY)
    response = co.chat(
        model="command-r-plus-08-2024", 
        messages=[
            {"role": "system", "message":  """
                Eres un profesor de matemáticas que explica teoremas de una manera sencilla. 
                Tu objetivo es proporcionar tres respuestas:
                1. Una explicación clara y comprensible del teorema, con un tono amistoso y accesible.
                2. Los conocimientos previos que los estudiantes deberían conocer para entender el teorema.
                3. Un ejemplo sencillo de cómo aplicar el teorema en un caso práctico.
                Evita tecnicismos complicados y trata de hacer la explicación divertida y fácil de recordar.
                """},
            {"role": "user", "content": theorem.teorema}
        ]
    )
    
    # Obtener la explicación desde la respuesta
    explanation = response.message.content[0].text
    explanation = explanation.replace('\n', ' ')

    # Connect to the database using environment variables
    db = pymysql.connect(host = "database-1.cdwam62w673f.eu-north-1.rds.amazonaws.com" ,
                    user = "admin",
                    password = "123456789",
                    cursorclass = pymysql.cursors.DictCursor
    )
    cursor = db.cursor()

    # Use the database
    cursor.execute("USE math_database")
    
    # Insert the theorem into the database
    query = """INSERT INTO theorem (theorem, respuesta) VALUES (%s, %s)"""
    
    # Accessing response text properly
    # explanation = response['message'][0]['text']
    
    cursor.execute(query, (theorem.teorema, explanation))
    db.commit()
    db.close()
    cursor.close()
    

    return explanation
    


if __name__ == "__main__":
    uvicorn.run("modelo_app:app", host="0.0.0.0", port=8000, reload=True)
