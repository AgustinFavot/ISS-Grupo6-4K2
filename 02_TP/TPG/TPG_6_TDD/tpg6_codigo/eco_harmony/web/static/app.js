"use strict";

const estado = {
  fecha: null,
  actividades: [],
  actividad: null,
  hora: null,
  cantidad: 1,
  visitantes: [],
};

const $ = (id) => document.getElementById(id);

function crear(etiqueta, atributos = {}, hijos = []) {
  const elemento = document.createElement(etiqueta);
  for (const [clave, valor] of Object.entries(atributos)) {
    if (clave === "texto") elemento.textContent = valor;
    else if (clave === "clase") elemento.className = valor;
    else if (valor !== false && valor !== null) elemento.setAttribute(clave, valor);
  }
  hijos.forEach((hijo) => elemento.append(hijo));
  return elemento;
}

function opcion(principal, detalle, { activa, deshabilitada, alElegir, etiqueta }) {
  const boton = crear("button", {
    type: "button",
    clase: "opcion",
    "aria-pressed": activa ? "true" : "false",
    "aria-label": etiqueta || null,
    disabled: deshabilitada ? "" : false,
  }, [
    crear("span", { clase: "opcion__principal", texto: principal }),
    crear("span", { clase: "opcion__detalle", texto: detalle }),
  ]);
  if (!deshabilitada) boton.addEventListener("click", alElegir);
  return boton;
}

const MOTIVOS_CORTOS = { "Parque cerrado": "Cerrado", "Fuera de las 24 hs": "" };
const formatoHora = (hora) => `${String(hora).padStart(2, "0")}:00`;
const formatoFecha = (iso) => iso.split("-").reverse().join("/");
const lugares = (n) => (n === 1 ? "1 lugar" : `${n} lugares`);

async function pedir(url, opciones) {
  const respuesta = await fetch(url, opciones);
  const datos = await respuesta.json();
  return { ok: respuesta.ok, datos };
}

function mostrarError(mensaje) {
  const caja = $("error");
  caja.textContent = mensaje || "";
  caja.hidden = !mensaje;
  if (mensaje) caja.scrollIntoView({ behavior: "smooth", block: "center" });
}

/* Paso 1: días (los cerrados o fuera de la ventana quedan deshabilitados) */
async function cargarDias() {
  const { datos } = await pedir("/api/dias");
  const contenedor = $("dias");
  contenedor.replaceChildren(...datos.map((dia) => {
    const boton = opcion(dia.dia, String(dia.numero), {
      activa: dia.fecha === estado.fecha,
      deshabilitada: !dia.habilitado,
      etiqueta: `${dia.dia} ${formatoFecha(dia.fecha)}${dia.habilitado ? "" : ", " + dia.motivo}`,
      alElegir: () => elegirDia(dia.fecha),
    });
    if (!dia.habilitado) {
      boton.title = dia.motivo;
      boton.append(crear("span", { clase: "opcion__motivo", texto: MOTIVOS_CORTOS[dia.motivo] ?? dia.motivo }));
    }
    return boton;
  }));
  const primero = datos.find((dia) => dia.habilitado);
  if (!estado.fecha && primero) elegirDia(primero.fecha);
  if (!primero) {
    contenedor.after(crear("p", { clase: "vacio", texto: "No hay turnos abiertos en las próximas 24 hs." }));
  }
}

async function elegirDia(fecha) {
  estado.fecha = fecha;
  mostrarError("");
  await cargarDias();
  const { datos } = await pedir(`/api/disponibilidad?fecha=${fecha}`);
  estado.actividades = datos.actividades;
  const sigue = actividadActual();
  if (!sigue || !tieneCupo(sigue)) estado.actividad = null;
  if (estado.actividad && !horarioActual()) estado.hora = null;
  dibujar();
}

const actividadActual = () => estado.actividades.find((a) => a.nombre === estado.actividad);
const horarioActual = () => actividadActual()?.horarios.find((h) => h.hora === estado.hora && h.cupos > 0);
const tieneCupo = (actividad) => actividad.horarios.some((h) => h.cupos > 0);

function detalleActividad(actividad) {
  if (!tieneCupo(actividad)) return "Sin cupo en este día";
  const partes = [];
  if (actividad.edad_minima) partes.push(`Desde ${actividad.edad_minima} años`);
  else partes.push("Todas las edades");
  if (actividad.requiere_talle) partes.push("Requiere talle");
  return partes.join(", ");
}

/* Paso 2: actividades, deshabilitadas si no tienen cupo en el día */
function dibujarActividades() {
  $("paso-actividad").hidden = !estado.fecha;
  $("actividades").replaceChildren(...estado.actividades.map((actividad) => {
    const libres = actividad.horarios.reduce((suma, h) => suma + h.cupos, 0);
    const total = actividad.horarios.length * actividad.cupo_por_turno || 1;
    const boton = opcion(actividad.nombre, detalleActividad(actividad), {
      activa: actividad.nombre === estado.actividad,
      deshabilitada: !tieneCupo(actividad),
      alElegir: () => {
        estado.actividad = actividad.nombre;
        if (!horarioActual()) estado.hora = null;
        mostrarError("");
        dibujar();
      },
    });
    const barra = crear("span", { clase: "cupo", "aria-hidden": "true" }, [crear("span")]);
    barra.firstChild.style.width = `${Math.round((libres / total) * 100)}%`;
    boton.append(barra);
    return boton;
  }));
}

/* Paso 3: horarios de la actividad, con los cupos visibles (FAQ 8) */
function dibujarHorarios() {
  const actividad = actividadActual();
  $("paso-horario").hidden = !actividad;
  if (!actividad) return;
  $("horarios").replaceChildren(...actividad.horarios.map((horario) => opcion(
    formatoHora(horario.hora),
    horario.cupos > 0 ? lugares(horario.cupos) : "Completo",
    {
      activa: horario.hora === estado.hora,
      deshabilitada: horario.cupos === 0,
      alElegir: () => {
        estado.hora = horario.hora;
        estado.cantidad = Math.min(estado.cantidad, horario.cupos);
        mostrarError("");
        dibujar();
      },
    },
  )));
}

/* Paso 4: cantidad de personas y datos de cada visitante */
function guardarVisitantes() {
  document.querySelectorAll(".visitante").forEach((grupo, i) => {
    estado.visitantes[i] = {
      nombre: grupo.querySelector("[name=nombre]").value,
      dni: grupo.querySelector("[name=dni]").value,
      edad: grupo.querySelector("[name=edad]").value,
      talle: grupo.querySelector("[name=talle]")?.value || "",
    };
  });
}

function campo(etiqueta, control, ayuda, clase = "campo") {
  const id = `c-${Math.random().toString(36).slice(2, 9)}`;
  control.id = id;
  const hijos = [crear("label", { for: id, texto: etiqueta }), control];
  if (ayuda) hijos.push(crear("span", { clase: "ayuda", texto: ayuda }));
  return crear("div", { clase }, hijos);
}

function dibujarVisitantes() {
  const horario = horarioActual();
  $("paso-personas").hidden = !horario;
  if (!horario) return;
  const actividad = actividadActual();
  guardarVisitantes();
  $("cantidad").textContent = estado.cantidad;
  $("menos").disabled = estado.cantidad <= 1;
  $("mas").disabled = estado.cantidad >= horario.cupos;
  $("cupo-restante").textContent = `Quedan ${lugares(horario.cupos)} en este turno.`;

  const grupos = [];
  for (let i = 0; i < estado.cantidad; i += 1) {
    const previo = estado.visitantes[i] || {};
    const hijos = [
      crear("legend", { texto: `Persona ${i + 1}` }),
      campo("Nombre", crear("input", { name: "nombre", autocomplete: "name", required: "", value: previo.nombre || "" }), "", "campo ancho"),
      campo("DNI", crear("input", { name: "dni", inputmode: "numeric", pattern: "\\d{7,8}", maxlength: "8", required: "", value: previo.dni || "" }), "7 u 8 números, sin puntos"),
      campo("Edad", crear("input", { name: "edad", type: "number", min: String(actividad.edad_minima), max: "120", inputmode: "numeric", required: "", value: previo.edad ?? "" }),
        actividad.edad_minima ? `Desde ${actividad.edad_minima} años` : ""),
    ];
    if (actividad.requiere_talle) {
      const selector = crear("select", { name: "talle", required: "" }, [
        crear("option", { value: "", texto: "Elegí un talle" }),
        ...window.TALLES.map((talle) => crear("option", { value: talle, texto: talle, selected: previo.talle === talle ? "" : false })),
      ]);
      hijos.push(campo("Talle de vestimenta", selector, "", "campo ancho"));
    }
    grupos.push(crear("fieldset", { clase: "visitante" }, hijos));
  }
  $("visitantes").replaceChildren(...grupos);
}

/* Paso 5: términos específicos de la actividad */
function dibujarTerminos() {
  const actividad = actividadActual();
  const visible = Boolean(horarioActual());
  $("paso-terminos").hidden = !visible;
  $("enviar").hidden = !visible;
  if (!visible) return;
  $("terminos-texto").textContent = actividad.terminos;
  $("acepta-texto").textContent = `Acepto los términos y condiciones de ${actividad.nombre}`;
}

function dibujar() {
  dibujarActividades();
  dibujarHorarios();
  dibujarVisitantes();
  dibujarTerminos();
}

function cambiarCantidad(delta) {
  guardarVisitantes();
  const horario = horarioActual();
  estado.cantidad = Math.max(1, Math.min(horario.cupos, estado.cantidad + delta));
  dibujarVisitantes();
}

async function enviar(evento) {
  evento.preventDefault();
  guardarVisitantes();
  const boton = $("enviar");
  boton.disabled = true;
  boton.textContent = "Inscribiendo…";
  try {
    const { ok, datos } = await pedir("/api/inscripciones", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        actividad: estado.actividad,
        fecha: estado.fecha,
        hora: estado.hora,
        cantidad: estado.cantidad,
        visitantes: estado.visitantes.slice(0, estado.cantidad),
        acepta_terminos: $("acepta").checked,
      }),
    });
    if (!ok) {
      mostrarError(datos.error);
      return;
    }
    mostrarError("");
    mostrarConfirmacion(datos);
  } catch {
    mostrarError("No se pudo conectar con el servidor. Revisá la conexión e intentá de nuevo.");
  } finally {
    boton.disabled = false;
    boton.textContent = "Inscribirme";
  }
}

function mostrarConfirmacion({ inscripcion, mail }) {
  $("c-mail").textContent = mail.destinatario;
  $("c-resumen").textContent =
    `Inscripción N° ${inscripcion.numero}: ${inscripcion.actividad}, ${formatoFecha(inscripcion.fecha)} a las ${formatoHora(inscripcion.hora)}.`;
  $("c-entradas").replaceChildren(...inscripcion.visitantes.map((v) => {
    const qr = crear("div", { clase: "entrada__qr", role: "img", "aria-label": `Código QR de ${v.nombre}` });
    qr.innerHTML = v.qr_svg; // SVG generado por el servidor, sin datos del usuario
    const detalle = `DNI ${v.dni}, ${v.edad} años${v.talle ? `, talle ${v.talle}` : ""}`;
    return crear("article", { clase: "entrada" }, [
      crear("div", { clase: "entrada__datos" }, [
        crear("div", { clase: "entrada__actividad", texto: `${inscripcion.actividad} ${formatoHora(inscripcion.hora)}` }),
        crear("div", { clase: "entrada__nombre", texto: v.nombre }),
        crear("div", { clase: "nota", texto: detalle }),
        crear("div", { clase: "entrada__codigo", texto: v.qr }),
      ]),
      qr,
    ]);
  }));
  $("c-asunto").textContent = mail.asunto;
  $("c-cuerpo").textContent = mail.cuerpo;
  $("confirmacion").showModal();
}

function reiniciar() {
  $("confirmacion").close();
  estado.hora = null;
  estado.cantidad = 1;
  estado.visitantes = [];
  $("acepta").checked = false;
  elegirDia(estado.fecha);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

$("menos").addEventListener("click", () => cambiarCantidad(-1));
$("mas").addEventListener("click", () => cambiarCantidad(1));
$("formulario").addEventListener("submit", enviar);
$("cerrar").addEventListener("click", reiniciar);
cargarDias();
