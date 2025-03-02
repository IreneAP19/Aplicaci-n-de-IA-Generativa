import streamlit as st
import requests

# URL de la API FastAPI
API_URL = "http://127.0.0.1:8000/add_theorem"

# Título de la aplicación
st.title("API de Teoremas de Matemáticas")

# Campo para ingresar el teorema
teorema = st.text_area("Ingresa el teorema que deseas agregar:")

# Botón para enviar el teorema
if st.button("Enviar Teorema"):
    if teorema:
        # Hacer la solicitud POST a la API de FastAPI
        response = requests.post(API_URL, json={"teorema": teorema})

        # Verifica si la respuesta es exitosa (200 OK)
        if response.status_code == 200:
            # Mostrar la respuesta de la API (que es el texto de la explicación)
            st.success("Teorema añadido correctamente!")
            
            # Remplazar \n por saltos de línea reales para mejorar la visualización
            explanation = response.text.replace("\n", "<br>")  # Reemplazamos \n por <br> para HTML
            
            # Mostrar la explicación usando markdown
            st.markdown(f"Explicación: {explanation}", unsafe_allow_html=True)

        else:
            st.error(f"Error en la API: {response.status_code}")
    else:
        st.warning("Por favor ingresa un teorema.")
