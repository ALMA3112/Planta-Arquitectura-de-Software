const URL_BASE = "http://127.0.0.1:5000/api/v1";

async function cargarEspecies() {
  const selectEspecie = document.getElementById("especie");

  try {
    const respuesta = await fetch(`${URL_BASE}/especies`);
    const especies = await respuesta.json();

    selectEspecie.innerHTML = "";

    especies.forEach((especie) => {
      const opcion = document.createElement("option");
      opcion.value = especie.nombre;
      opcion.textContent = especie.nombre;
      selectEspecie.appendChild(opcion);
    });
  } catch (error) {
    selectEspecie.innerHTML = '<option value="">Error al cargar especies</option>';
    console.error("Error cargando especies:", error);
  }
}

cargarEspecies();

const formulario = document.getElementById("formulario-diagnostico");
const divResultado = document.getElementById("resultado");
const divError = document.getElementById("error");

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  ocultarResultado();
  ocultarError();

  const datos = {
    especie: document.getElementById("especie").value,
    humedad: parseFloat(document.getElementById("humedad").value),
    luz: parseFloat(document.getElementById("luz").value),
    temperatura: parseFloat(document.getElementById("temperatura").value),
  };

  try {
    const respuesta = await fetch(`${URL_BASE}/diagnosticos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });

    const cuerpo = await respuesta.json();

    if (respuesta.ok) {
      mostrarResultado(cuerpo);
    } else {
      mostrarError(cuerpo);
    }
  } catch (error) {
    mostrarError({
      error: "ERROR_DE_CONEXION",
      mensaje: "No se pudo conectar con el servidor. ¿Está corriendo el backend?",
    });
  }
});

function ocultarResultado() {
  divResultado.className = "";
  divResultado.innerHTML = "";
}

function ocultarError() {
  divError.className = "";
  divError.innerHTML = "";
}

function mostrarResultado(datos) {
  const claseEstado = datos.estado.toLowerCase();
  divResultado.className = claseEstado;

  let html = `<h3>Estado: ${datos.estado}</h3>`;

  datos.parametros.forEach((p) => {
    html += `<div class="parametro"><strong>${p.nombre}:</strong> ${p.valor} ${p.unidad} → ${p.estado} (óptimo: ${p.rangoOptimo[0]}-${p.rangoOptimo[1]})</div>`;
  });

  if (datos.recomendaciones.length > 0) {
    html += `<div class="recomendacion"><strong>Recomendaciones:</strong><ul>`;
    datos.recomendaciones.forEach((r) => {
      html += `<li>${r}</li>`;
    });
    html += `</ul></div>`;
  }

  divResultado.innerHTML = html;
}

function mostrarError(datos) {
  divError.className = "visible";
  divError.innerHTML = `<strong>${datos.error || "ERROR"}:</strong> ${datos.mensaje}`;
}

