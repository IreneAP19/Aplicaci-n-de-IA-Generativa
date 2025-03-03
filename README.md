# Aplicación Web de Explicación de Teoremas Matemáticos
![Texto alternativo](app/static/img/logo.png)

Este proyecto consiste en una aplicación web que permite a los usuarios interactuar con el modelo de LLM Cohere para obtener explicaciones sencillas de teoremas matemáticos. Utiliza FastAPI para crear la API y una base de datos en AWS para almacenar el historial de interacciones de los usuarios.

## Tabla de Contenidos
- [Descripción](#descripción)
- [Características](#características)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Requisitos Previos](#Requisitos-Previosn)

## Descripción

Este proyecto tiene como objetivo proporcionar una herramienta interactiva para estudiantes de matemáticas o cualquier persona interesada en aprender de manera más sencilla sobre teoremas matemáticos. El usuario puede ingresar un teorema matemático, y la aplicación proporciona:
- Una explicación sencilla del teorema.
- Los conceptos previos necesarios para entender el teorema.
- Un ejemplo práctico que muestra cómo aplicar el teorema.

La aplicación utiliza modelos pre-entrenado **Cohere**. Además, se almacena el historial de las interacciones de los usuarios en una base de datos de AWS para su análisis y personalización futura.

## Características
- **Explicaciones sencillas** de teoremas matemáticos.
- **Generación de ejemplos prácticos** para ilustrar teoremas.
- **Almacenamiento de interacciones** de los usuarios en una base de datos de AWS.
- **Despliegue escalable** usando Docker y DockerHub.

## Tecnologías Utilizadas
- **Python**: Lenguaje de programación principal.
- **FastAPI**: Framework para construir la API web de alto rendimiento.
- **Cohere**: Plataforma para acceder a modelos pre-entrenados de lenguaje.
- **AWS**: Base de datos en la nube para almacenar el historial de interacciones.
- **Docker**: Contenerización de la aplicación para facilitar el despliegue y escalabilidad.
- **DockerHub**: Repositorio para subir las imágenes Docker.
- **GitHub**: Control de versiones y repositorio de código fuente.

## Requisitos Previos
- Cuenta en AWS para crear la base de datos
- Docker (opcional, si deseas dockerizar la aplicación)
- Cuenta en Cohere para obtener la clave API

## Documentos
- **Static**: Encontramos los documentos necesarios para hacer el front
- **Templates**: Documento en .html donde se ha creado en front de la aplicación 
- **Test**: Tenemos diversos test, fundamentales para asegurarse de que la API funcione correctamente, que las rutas devuelvan los resultados esperados y que la lógica esté funcionando como se espera.
- **BBDD**: Tenemos la creación de la base de datos conectada a AWS que hemos creado con SQL
- **modelo_app_html.py**: Encontramos la programación de la FastApi
  
