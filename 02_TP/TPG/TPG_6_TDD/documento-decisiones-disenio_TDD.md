# TP6 – TDD: Inscribirme a actividad

Oct 19, 2026 · @Agus

## 1. Datos generales

Se implementó la User Story **Inscribirme a actividad** (5 SP, grupos pares) del dominio EcoHarmony Park aplicando el ciclo Red-Green-Refactor.

| Aspecto | Definición |
| --- | --- |
| User Story | COMO visitante QUIERO inscribirme a una actividad PARA reservar mi lugar en la misma |
| Lenguaje | Python 3 (supuesto: reemplazar por el lenguaje elegido en el TP2) |
| Framework de pruebas | pytest |
| Guía de estilos | PEP 8, con tipado estático (supuesto: reemplazar por la guía elegida en el TP2) |
| Dependencias externas | Flask (interfaz web), qrcode (imágenes QR) y pytest (pruebas) |
| Sesión y usuario | Mockeados, según FAQ 19 |
| Envío de mail | Simulado, según FAQ 5 |

**Entradas faltantes.** El lenguaje y el documento de estilos del TP2 no forman parte del material disponible. Se eligió Python por ser el lenguaje del ejemplo de clase (Taxi Mobile). El diseño no depende del lenguaje y se traslada sin cambios conceptuales.

## 2. Reglas de negocio implementadas

La implementación cubre los seis criterios de aceptación de la tarjeta y las reglas del FAQ que los precisan. Cada regla se valida con una excepción específica.

| Regla | Valor implementado | Fuente | Excepción |
| --- | --- | --- | --- |
| Actividades ofrecidas | Tirolesa, Safari, Palestra, Jardinería | CA 1 | `ActividadInexistenteError` |
| Cupo por turno | Safari 8, Palestra 12, Jardinería 12, Tirolesa 10 | CA 1, FAQ 13 | `SinCupoError` |
| Visibilidad de cupos | Consulta de cupos, actividades y horarios disponibles | CA 1 y 2, FAQ 8 | — |
| Días cerrados | Lunes, 25/12 y 1/1 | FAQ 1 | `ParqueCerradoError` |
| Turnos | Uno por hora, de 9 a 17; a las 18 no hay turno | CA 2, FAQ 12 | `HorarioNoDisponibleError` |
| Anticipación máxima | El turno debe empezar dentro de las próximas 24 hs | FAQ 23 | `FueraDeVentanaError` |
| Cierre de inscripción | Hasta 15 minutos antes del inicio | FAQ 30 | `FueraDeVentanaError` |
| Cantidad de personas | Al menos 1 y coincidente con los visitantes; sin máximo salvo el cupo | CA 3, FAQ 31 | `CantidadPersonasInvalidaError` |
| Datos del visitante | Nombre, DNI y edad obligatorios; solo DNI | CA 4, FAQ 32 | `DatosVisitanteInvalidosError` |
| Talle de vestimenta | Obligatorio en Palestra y Tirolesa | CA 4, FAQ 9 | `TalleRequeridoError` |
| Talles válidos | XS, S, M, L, XL, XXL | FAQ 14 | `TalleInvalidoError` |
| Edad mínima | Palestra 12, Tirolesa 8, resto sin límite | FAQ 15 | `EdadInsuficienteError` |
| Superposición | Un DNI no puede tener dos inscripciones en el mismo horario | FAQ 29 | `SuperposicionHorariaError` |
| Términos y condiciones | Aceptación obligatoria | CA 5 | `TerminosNoAceptadosError` |
| Mail de confirmación | Resumen de la inscripción y un QR por participante | CA 6, FAQ 28 | — |

Quedan fuera de alcance el registro y login (FAQ 19). Los textos de términos y el logo (FAQ 16 y 17) se incluyen como borrador pendiente de validación del PO. El nombre opcional de la persona a cargo de la actividad (FAQ 22) no se incluyó por ser opcional.

## 3. Interpretaciones y supuestos

Los siguientes puntos no están definidos de forma unívoca en la documentación. Se tomó la interpretación indicada y se dejó cubierta por pruebas, de modo que un cambio de criterio del PO se refleje en un solo lugar.

| Punto | Interpretación adoptada | Motivo |
| --- | --- | --- |
| Ventana de 24 hs (FAQ 23) | Se acepta si el turno empieza dentro de las próximas 24 hs; exactamente 24 hs se acepta | El ejemplo del FAQ (martes → viernes, no) indica una cota máxima de anticipación |
| Cierre de 15 minutos (FAQ 30) | Exactamente 15 minutos antes se acepta; a partir de 14 min 59 s se rechaza | "15 minutos antes" se toma como último instante válido |
| Formato del DNI (FAQ 32) | Solo dígitos, 7 u 8 caracteres | El FAQ descarta pasaportes; la longitud es un supuesto del grupo |
| QR (CA 6, FAQ 28) | Un código por participante con formato `EHP-ACT-<número>-<DNI>` | El FAQ habla de "los QR"; la imagen QR no se genera porque el mail es simulado |
| Destinatario del mail | El email del titular logueado (usuario mockeado) | La US no pide email por participante |
| Superposición (FAQ 29) | Mismo DNI en la misma fecha y hora, en cualquier actividad, incluida la misma | Todas las actividades duran una hora y empiezan en punto |
| Talle en actividades que no lo requieren | Se acepta si se informa y no se valida | La prueba de usuario solo exige que su ausencia pase |
| Validez de la edad | Entero mayor o igual a 0 | Safari y Jardinería admiten todas las edades (FAQ 15) |

El horario del parque (8:30 a 19, FAQ 11) no se aplica a la inscripción porque la regla específica de la US son los turnos y las ventanas de 24 hs y 15 minutos.

## 4. Diseño: módulos y responsabilidades

El código se organiza en un servicio de aplicación que coordina entidades inmutables y dos dependencias externas inyectadas (reloj y notificador).

| Módulo | Elementos | Responsabilidad |
| --- | --- | --- |
| `dominio.py` | `Actividad`, `Turno`, `Visitante`, `Usuario`, `Inscripcion`, `CATALOGO_ACTIVIDADES`, `TALLES_VALIDOS`, `generar_codigo_qr` | Entidades y datos del dominio |
| `calendario.py` | `parque_abierto`, `es_hora_de_turno`, `horas_de_turno` | Días de apertura y horario de turnos |
| `servicio.py` | `ServicioInscripcion` | Consultas de disponibilidad, validaciones e inscripción |
| `repositorio.py` | `RepositorioInscripciones` | Guarda inscripciones; cuenta lugares ocupados y DNI por turno |
| `mensajes.py` | `componer_confirmacion` | Arma asunto y cuerpo del mail con resumen y QR |
| `puertos.py` | `Reloj`, `Notificador`, `RelojSistema`, `NotificadorSimulado` | Contratos de las dependencias externas y su versión real |
| `errores.py` | `InscripcionError` y 12 subclases | Una excepción por regla de negocio |

La operación principal es `ServicioInscripcion.inscribir(titular, actividad, fecha, hora, cantidad_personas, visitantes, acepta_terminos)`. Ejecuta las validaciones en este orden:

1. Actividad existente.
2. Turno válido: parque abierto, hora de turno y ventana de 24 hs / 15 min.
3. Cantidad de personas coincidente con los visitantes.
4. Datos de cada visitante: nombre, DNI, edad, edad mínima y talle.
5. Cupo restante del turno.
6. Superposición horaria por DNI.
7. Aceptación de términos y condiciones.
8. Registro de la inscripción, generación de los QR y envío del mail.

Las consultas `cupos_disponibles`, `actividades_disponibles` y `horarios_disponibles` resuelven los criterios de selección (CA 1 y 2) reutilizando las mismas reglas de turno y cupo.

| Módulo | Elementos | Responsabilidad |
| --- | --- | --- |
| `web/__init__.py` | `crear_app` y rutas `/`, `/api/dias`, `/api/disponibilidad`, `/api/inscripciones` | Interfaz: traduce HTTP a llamadas al servicio y errores a respuestas 400 / 422 |
| `web/terminos.py` | `TERMINOS_Y_CONDICIONES` | Texto de términos por actividad |
| `web/templates`, `web/static` | `index.html`, `app.css`, `app.js`, `logo.svg` | Pantalla responsive del flujo de inscripción |

La interfaz no contiene reglas de negocio: todas las validaciones siguen en `ServicioInscripcion`, por eso las pruebas de dominio no cambiaron al agregarla.

## 5. Decisiones de diseño

**Reloj inyectado.** El servicio recibe un objeto con el método `ahora()` en lugar de leer la hora del sistema. Las reglas de lunes, feriados, 24 hs y 15 minutos dependen del momento actual; con un `RelojFijo` cada prueba fija ese momento y el resultado es siempre el mismo (*Isolated test*).

**Notificador inyectado y simulado.** El mail se envía a través de la interfaz `Notificador`. En ejecución se usa `NotificadorSimulado`, que informa "Mail enviado a …" como permite el FAQ 5. En las pruebas, un `NotificadorEspia` registra los mails para verificar destinatario, resumen y QR.

**Una excepción por regla.** Cada regla tiene su excepción, todas derivadas de `InscripcionError`. Las pruebas verifican el motivo exacto del rechazo y no solo que "algo falló"; la interfaz puede capturar la clase base para mostrar el mensaje.

**Validar todo antes de registrar.** La inscripción se guarda y el mail se envía solo después de superar todas las validaciones. Una inscripción rechazada no ocupa cupo ni genera mail, y hay una prueba que lo verifica.

**Reglas como datos.** Cupos, talle requerido y edad mínima son atributos de `Actividad` dentro de un catálogo. Agregar o modificar una actividad no requiere tocar la lógica, a diferencia de la cadena de condicionales del ejemplo final de Taxi Mobile.

**Entidades inmutables.** Las clases del dominio son `dataclass(frozen=True)`. Una inscripción confirmada no puede alterarse por error y las entidades se comparan por valor, lo que simplifica las aserciones.

**Repositorio en memoria.** No hay persistencia en el alcance de la US. El repositorio aísla el almacenamiento: reemplazarlo por una base de datos no cambia el servicio ni las pruebas de reglas.

**Responsabilidad única.** El calendario, la composición del mail y el almacenamiento están en módulos propios. El servicio solo coordina y valida.

## 6. Interfaz de usuario

La US se usa desde una interfaz web responsive, que el FAQ 24 admite en lugar de una app móvil nativa. Se levanta con `python app.py` y guía al visitante en cinco pasos sobre una sola pantalla.

1. **Elegí el día.** Calendario de 7 días. Los días cerrados (lunes, 25/12 y 1/1) y los que todavía no abren inscripción quedan tachados y no se pueden seleccionar (FAQ 2).
2. **Elegí la actividad.** Las cuatro actividades con su edad mínima, si requieren talle y una barra con los lugares libres del día. Una actividad sin cupo queda deshabilitada (CA 1).
3. **Elegí el horario.** Turnos de 9 a 17 con los lugares restantes; los completos quedan deshabilitados (CA 2, FAQ 8).
4. **Participantes.** Selector de cantidad limitado al cupo del turno y un formulario por persona con nombre, DNI, edad y, solo si la actividad lo exige, talle (CA 3 y 4).
5. **Términos y condiciones.** Texto específico de la actividad y casilla de aceptación (CA 5).

Al confirmar se muestra el modal "Mail enviado a …" (FAQ 5) con un talón por participante que incluye su código QR, y el texto completo del mail simulado (CA 6). Si el servidor rechaza la inscripción, el motivo aparece sobre el botón e indica a qué participante corresponde, por ejemplo "Lucía: Palestra requiere 12 años o más."

| Pedido del PO | Cómo se resolvió |
| --- | --- |
| Paleta (FAQ 3) | Los cinco colores como variables CSS: verde bosque para encabezado y botones, ladrillo para errores y días cerrados |
| Fuente Lato (FAQ 3) | Google Fonts, con fuentes del sistema como respaldo sin conexión |
| Logo (FAQ 17) | Brote de dos hojas en SVG, como borrador para validar |
| Responsive (FAQ 24) | Columna única de hasta 36 rem; verificada a 390 px y a 1280 px de ancho |
| Cupos visibles (FAQ 8) | Lugares libres por actividad y por turno |

**Decisiones de la interfaz**

- **La interfaz no valida reglas de negocio.** El navegador solo arma la solicitud; el servidor llama a `ServicioInscripcion` y devuelve 422 con el motivo. Las reglas quedan en un solo lugar, ya cubierto por las pruebas de dominio.
- **Flask y JavaScript sin framework.** El flujo es una sola pantalla y no justifica la dependencia de un framework de frontend. Los datos del usuario se insertan con `textContent`, nunca como HTML.
- **Hora fijable para demostraciones.** La variable de entorno `ECO_AHORA` fija el reloj, igual que `RelojFijo` en las pruebas. Sirve para mostrar turnos abiertos aunque la demostración sea un lunes o de noche.
- **Usuario mockeado.** El titular es fijo (Ana Pérez), según el FAQ 19; su email es el destinatario del mail simulado.

## 7. Aplicación del ciclo TDD

El desarrollo partió de una lista de pruebas ordenada de menor a mayor complejidad (*One step*). Cada ítem se resolvió con un ciclo Red-Green-Refactor; los casos que surgieron en el camino se anotaron al final de la lista (*Another test*).

### Lista de pruebas

1. Inscripción exitosa a una actividad sin talle (*Starter test*).
2. Rechazo por no aceptar términos y condiciones.
3. Rechazo por actividad inexistente.
4. Rechazo por falta de talle en Palestra y Tirolesa; talles válidos e inválidos.
5. Rechazo por turno sin cupo; cupo completo exacto por actividad; cupo independiente por turno.
6. Rechazo por día cerrado: lunes, 25/12 y 1/1.
7. Rechazo por hora fuera de turno: 8, 18 y 19; turnos límite 9 y 17 aceptados.
8. Ventana de inscripción: límites de 24 hs y de 15 minutos; turno ya iniciado.
9. Edad mínima: límites 11/12 en Palestra y 7/8 en Tirolesa.
10. Datos de visitante inválidos y cantidad de personas no coincidente.
11. Superposición horaria por DNI.
12. Mail con resumen y un QR por participante.
13. Consultas de cupos, actividades y horarios disponibles.
14. Una inscripción rechazada no ocupa cupo ni envía mail.

### Ciclo 1: inscripción exitosa (Starter test)

**RED.** Se declara la intención: con datos válidos, el sistema devuelve una inscripción a Jardinería sin talle. El test falla porque `ServicioInscripcion` no existe; según la segunda ley, no compilar también cuenta como fallo.

```python
def test_inscribirse_sin_talle_cuando_la_actividad_no_lo_requiere_pasa(inscribir):
    inscripcion = inscribir(actividad="Jardinería",
                            visitantes=[crear_visitante(talle=None)])

    assert inscripcion.visitantes[0].talle is None
```

**GREEN.** *Fake it*: `inscribir` devuelve una `Inscripcion` armada con los visitantes recibidos, sin ninguna validación.

**REFACTOR.** Se crean las entidades `Actividad`, `Turno` y `Visitante` y el catálogo de actividades. El test sigue en verde.

### Ciclo 2: términos y condiciones (Obvious implementation)

**RED.** `inscribir(acepta_terminos=False)` debe lanzar `TerminosNoAceptadosError`; falla porque la excepción no existe.

**GREEN.** La implementación es evidente: `if not acepta_terminos: raise TerminosNoAceptadosError(...)`.

**REFACTOR.** Se crea la clase base `InscripcionError`, que luego agrupa todas las excepciones de reglas.

### Ciclo 3: cupos (Triangulación y One-to-many)

**RED.** Se inscriben 8 personas en Safari a las 10 y luego una más; se espera `SinCupoError`.

**GREEN.** Primero se resolvió para una sola actividad con un contador. La triangulación con dos pruebas más obligó a generalizar: el cupo exacto de las cuatro actividades (prueba parametrizada) y el cupo independiente por turno. Así el conteo pasó a hacerse por actividad y turno sobre las inscripciones guardadas.

**REFACTOR.** El almacenamiento se extrajo a `RepositorioInscripciones` y el cálculo a `cupos_disponibles`, que después reutilizan las consultas de actividades y horarios disponibles.

### Ciclo 4: ventana de 24 hs y 15 minutos (Expedition test)

**RED.** Al escribir la prueba del cierre de 15 minutos surgió el debate de cómo probar algo que depende de la hora real. Se resolvió con una prueba que fija el momento actual:

```python
def test_inscribirse_a_menos_de_15_minutos_del_turno_falla(inscribir, reloj):
    reloj.momento = datetime(2026, 10, 20, 9, 46)

    with pytest.raises(FueraDeVentanaError):
        inscribir(hora=10)
```

**GREEN.** Se compara el inicio del turno con `reloj.ahora()` usando dos constantes: `CIERRE_PREVIO_AL_TURNO` (15 min) y `ANTICIPACION_MAXIMA` (24 hs).

**REFACTOR.** El reloj pasó a ser una dependencia del constructor (`Reloj`), con `RelojSistema` para ejecución y `RelojFijo` para pruebas. Las pruebas de límite exacto (9:45 pasa, 9:46 falla) fijan la interpretación de la sección 3.

### Ciclo 5: interfaz web (Test first sobre la API)

**RED.** Las pruebas de la interfaz se escribieron antes que el módulo `web`, con el cliente de pruebas de Flask: días deshabilitados, cupos visibles, inscripción con QR y mail, rechazo 422 con motivo y solicitudes mal formadas con 400. Fallaron al no existir `crear_app`.

```python
def test_regla_de_negocio_incumplida_responde_422_con_motivo(cliente):
    respuesta = cliente.post("/api/inscripciones",
                             json=solicitud_valida(acepta_terminos=False))

    assert respuesta.status_code == 422
    assert respuesta.json["tipo"] == "TerminosNoAceptadosError"
```

**GREEN.** Se implementaron las rutas delegando en `ServicioInscripcion` y traduciendo `InscripcionError` a 422.

**REFACTOR.** La consulta privada `_turno_habilitado` pasó a ser pública (`turno_habilitado`) porque la necesita el calendario, y los mensajes de error pasaron a nombrar al participante. Las 59 pruebas de dominio siguieron en verde.

### Patrones aplicados

| Fase | Patrón | Dónde se aplicó |
| --- | --- | --- |
| RED | Starter test | Ciclo 1 |
| RED | One step | Orden de la lista de pruebas |
| RED | Expedition test | Ciclo 4: cómo probar reglas que dependen del tiempo |
| RED | Another test | DNI repetido en la misma inscripción e inscripción rechazada sin efectos, anotados al final |
| GREEN | Fake it | Ciclo 1 |
| GREEN | Obvious implementation | Ciclo 2 y validación de datos del visitante |
| GREEN | Triangulación | Cupos, edades mínimas y límites de ventana |
| GREEN | One-to-many | Cupo de una actividad generalizado a las cuatro |
| Diseño | Isolated test | Fixtures nuevas por prueba; reloj y notificador falsos |
| Diseño | Test data y Evident data | Fecha fija (martes 20/10/2026), DNI y edades que hacen visible la regla probada |
| Diseño | Assert first | Las pruebas de mail se escribieron desde la aserción sobre el cuerpo esperado |

Cada prueba sigue la estructura vista en clase: precondiciones (fixtures y reloj), pasos (la llamada a `inscribir`) y resultado (`assert` o `pytest.raises`).

## 8. Trazabilidad de pruebas

Las seis pruebas de usuario de la tarjeta están automatizadas en `tests/test_pruebas_de_usuario.py`. Las reglas del FAQ se cubren en los demás archivos.

| Prueba de usuario o regla | Resultado esperado | Test automatizado |
| --- | --- | --- |
| Inscribirse con cupo, horario, datos, talle, términos y mail | Pasa | `test_inscribirse_con_cupo_datos_completos_y_terminos_pasa` |
| Actividad sin cupo en el horario | Falla | `test_inscribirse_a_turno_sin_cupo_falla` |
| Sin talle porque la actividad no lo requiere | Pasa | `test_inscribirse_sin_talle_cuando_la_actividad_no_lo_requiere_pasa` |
| Parque cerrado | Falla | `test_inscribirse_en_dia_que_el_parque_esta_cerrado_falla` |
| Actividad no disponible | Falla | `test_inscribirse_a_actividad_no_disponible_falla` |
| Horario no disponible | Falla | `test_inscribirse_fuera_del_horario_de_turnos_falla` |
| Sin aceptar términos | Falla | `test_inscribirse_sin_aceptar_terminos_falla` |
| Sin talle requerido | Falla | `test_inscribirse_sin_talle_requerido_por_la_actividad_falla` |
| Días cerrados: lunes, 25/12 y 1/1 (FAQ 1) | Falla | `test_inscribirse_en_dia_cerrado_falla` |
| Ventana de 24 hs (FAQ 23) | Pasa / falla | `test_inscribirse_exactamente_24_hs_antes_pasa`, `test_inscribirse_con_mas_de_24_hs_de_anticipacion_falla` |
| Cierre 15 minutos antes (FAQ 30) | Pasa / falla | `test_inscribirse_exactamente_15_minutos_antes_pasa`, `test_inscribirse_a_menos_de_15_minutos_del_turno_falla`, `test_inscribirse_a_turno_ya_iniciado_falla` |
| Cupo por actividad (FAQ 13) | Pasa / falla | `test_completar_exactamente_el_cupo_pasa`, `test_inscribir_mas_personas_que_el_cupo_restante_falla`, `test_el_cupo_es_independiente_por_turno` |
| Talles válidos (FAQ 14) | Pasa / falla | `test_talles_validos_pasan`, `test_talle_inexistente_falla` |
| Edad mínima (FAQ 15) | Pasa / falla | `test_edad_menor_a_la_minima_falla`, `test_edad_igual_a_la_minima_pasa`, `test_actividades_sin_limite_de_edad_aceptan_bebes` |
| Superposición horaria (FAQ 29) | Pasa / falla | `test_mismo_dni_en_otra_actividad_del_mismo_horario_falla`, `test_mismo_dni_en_distinto_horario_pasa`, `test_dni_repetido_dentro_de_la_misma_inscripcion_falla` |
| Sin máximo por transacción (FAQ 31) | Pasa | `test_inscribir_varias_personas_en_una_transaccion_pasa` |
| Datos del visitante y solo DNI (CA 4, FAQ 32) | Falla | `test_datos_de_visitante_invalidos_fallan`, `test_cantidad_que_no_coincide_con_visitantes_falla` |
| Mail con resumen y QR (CA 6, FAQ 28) | Pasa | `test_mail_contiene_resumen_y_un_qr_por_participante`, `test_cada_participante_recibe_un_qr_distinto`, `test_asunto_incluye_numero_de_inscripcion_y_actividad` |
| Selección de actividades y horarios con cupo (CA 1 y 2, FAQ 8) | Pasa | `test_actividades_disponibles_excluye_las_que_no_tienen_cupo`, `test_horarios_disponibles_excluye_turnos_sin_cupo`, `test_horarios_disponibles_respeta_ventana_y_cierre`, `test_cupos_disponibles_descuenta_los_inscriptos` |
| Rechazo sin efectos secundarios | Pasa | `test_inscripcion_rechazada_no_ocupa_cupo_ni_envia_mail` |

Las pruebas de la interfaz están en `tests/test_web.py`.

| Comportamiento de la interfaz | Resultado esperado | Test automatizado |
| --- | --- | --- |
| Fuente Lato y paleta del PO | Pasa | `test_pagina_principal_usa_fuente_y_paleta_del_po` |
| Calendario con días deshabilitados y su motivo (FAQ 2) | Pasa | `test_calendario_deshabilita_lunes_y_dias_fuera_de_ventana` |
| Cupos por turno y términos por actividad | Pasa | `test_disponibilidad_informa_cupos_y_terminos_por_actividad` |
| El cupo mostrado baja tras inscribirse | Pasa | `test_inscripcion_descuenta_el_cupo_mostrado` |
| Inscripción con QR y mail simulado | Pasa | `test_inscripcion_valida_devuelve_qr_y_mail_simulado` |
| Regla incumplida informada con su motivo | Falla (422) | `test_regla_de_negocio_incumplida_responde_422_con_motivo`, `test_talle_faltante_responde_422` |
| Datos mal formados | Falla (400) | `test_solicitud_mal_formada_responde_400`, `test_disponibilidad_con_fecha_invalida_responde_400` |

## 9. Ejecución y limitaciones

Las 70 pruebas automatizadas (59 de dominio y 11 de interfaz) pasan con Python 3.12 y pytest. La cobertura del código de producción es del 98 %; las líneas sin cubrir son el reloj y el notificador reales y la lectura de \`ECO\_AHORA\`, que en las pruebas se reemplazan por dobles. Además, el flujo completo se recorrió en un navegador a 390 px y a 1280 px de ancho. El código no presenta observaciones de `flake8` (PEP 8).

```
pip install -r requirements.txt
python -m pytest -v
python app.py   # http://127.0.0.1:5000
```

Como control adicional, se desactivó la validación de edad mínima y las dos pruebas de edad insuficiente fallaron; al restaurarla volvieron a pasar.

**Limitaciones**

- El lenguaje y la guía de estilos son supuestos; deben ajustarse a lo elegido en el TP2.
- El mail y el QR son simulados: el QR es el contenido del código, no una imagen.
- No hay persistencia: las inscripciones se pierden al reiniciar el servidor.
- El historial Red-Green-Refactor debe quedar registrado en el repositorio con un commit por fase, en la carpeta de Código Fuente del sprint definida en el TP4.
