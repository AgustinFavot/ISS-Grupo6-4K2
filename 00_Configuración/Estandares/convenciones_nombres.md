# Convenciones de Nombrado

Este documento es una referencia rápida a las reglas generales de nombrado definidas en el **Plan de Configuración (IC-02), Sección 5**.

## Resumen de reglas

| Regla | Patrón | Se aplica a |
|-------|--------|-------------|
| RN-01 | `<nombre>_v<MAJOR>.<MINOR>.md` | Documentos versionados (Plan SCM, Matriz de Trazabilidad) |
| RN-02 | `<tipo>_<AAAA-MM-DD>[_<tema>].md` | Minutas y anotaciones |
| RN-03 | `<tipo><nro>_isw_4k2_grupo6.<ext>` | Entregables grupales de TP y TIG |
| RN-04 | nombre original de la cátedra | Material provisto por la cátedra (sin modificar) |
| RN-05 | `<apellido_autor>-<titulo_abreviado>.<ext>` | Material bibliográfico externo |
| RN-06 | `convenciones-<tema>.md` | Archivos de convenciones del equipo |
| RN-07 | según la herramienta | Archivos de configuración técnica (.gitignore, *.yml) |
| RN-08 | `modelo_<tipo>_<tema>.<ext>` | Modelos de evaluación (parcial, final, coloquio) |
| RN-09 | `resumen_unidad<nro>_<tema>.md` | Resúmenes del equipo |
| RN-10 | `anotacion_<AAAA-MM-DD>_<tema>.md` | Anotaciones de clase |

## Convenciones generales

- **snake_case** para todos los nombres (palabras separadas por `_`), excepto donde la regla indique guiones.
- **Sin tildes ni ñ** en nombres de archivo.
- **Extensiones en minúsculas**: `.md`, `.pdf`, `.docx`, `.yml`.
- **Prefijo numérico en carpetas**: `NN_Nombre/` para mantener el orden visual.

## Definición de MAJOR y MINOR (para RN-01)

| Componente | Incrementar cuando... |
|------------|-----------------------|
| **MAJOR** | Cambio de fondo: nueva sección, cambio de estructura, nueva convención que impacta múltiples ICs. |
| **MINOR** | Ajuste menor: corrección ortográfica, aclaración de texto, actualización de un dato puntual. |

Al subir MAJOR, MINOR vuelve a 0.

## Ejemplos

| Tipo de archivo | Nombre correcto |
|-----------------|-----------------|
| Plan SCM versión 1, revisión 2 | `Plan_Configuracion_v1.2.md` |
| Minuta de TIG del 5 de sep. | `minuta_2026-09-05.md` |
| Entregable del TP5 | `tp5_isw_4k2_grupo6.pdf` |
| Resumen de Unidad 3 sobre SCM | `resumen_unidad3_scm.md` |
| Paper de Pressman (bibliografía) | `pressman-ingenieria_del_software.pdf` |
