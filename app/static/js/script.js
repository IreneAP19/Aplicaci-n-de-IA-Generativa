// Esta es la función para hacer una solicitud al backend y obtener la información del teorema
async function fetchTheorem() {
    const response = await fetch('/add_theorem', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            teorema: "Teorema de Pitágoras"
        })
    });

    const data = await response.json();
    // Insertar la respuesta en el HTML
    document.getElementById("explicacion").innerHTML = data.explicacion;
    document.getElementById("conocimientos_previos").innerHTML = data.conocimientos_previos;
    document.getElementById("ejemplo").innerHTML = data.ejemplo;
}

// Llamar a la función cuando la página se carga
window.onload = fetchTheorem;
