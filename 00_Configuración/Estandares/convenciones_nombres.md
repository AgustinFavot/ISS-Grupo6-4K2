# Convenciones de Nombrado

Este documento es una referencia rápida a las reglas generales de nombrado definidas en el **Plan de Configuración (IC-02), Sección 5**. Ante cualquier diferencia, el Plan es la fuente de verdad.

## Resumen de reglas

| Regla | Patrón | Se aplica a |
|-------|--------|-------------|
| RN-01 | `<nombre>_v<MAJOR>.<MINOR>.md` | Documentos versionados (Plan SCM, Matriz de Trazabilidad) |
| RN-02 | `<tipo>_<AAAA-MM-DD>[_<tema>].<ext>` | Documentos del equipo con fecha (minutas, anotaciones) |
| RN-03 | `<tipo><nro>_isw_4k2_grupo6.<ext>` | Entregables grupales de TP y TIG |
| RN-04 | nombre original de la cátedra | Material provisto por la cátedra (sin modificar) |
| RN-05 | `<tipo>_<tema>.<ext>` | Documentos del equipo sin fecha (resúmenes, modelos, convenciones) |
| RN-06 | según convención de la herramienta | Archivos de configuración técnica (`.gitignore`, `*.yml`) |

## Convenciones generales

- **snake_case** para todos los nombres (palabras separadas por `_`), salvo los archivos de configuración técnica (RN-06) y el material de cátedra (RN-04), que conservan su nombre original.
- **Sin tildes ni ñ** en nombres de archivo creados por el equipo.
- **Extensiones en minúsculas**: `.md`, `.pdf`, `.docx`, `.yml`.
- **Prefijo numérico en carpetas**: `NN_Nombre/` para mantener el orden visual.

## Definición de MAJOR y MINOR (para RN-01)

| Componente | Incrementar cuando... |
|------------|-----------------------|
| **MAJOR** | Cambio de fondo: nueva sección, cambio de estructura, nueva convención que impacta múltiples ICs. |
| **MINOR** | Ajuste menor: corrección ortográfica, aclaración de texto, actualización de un dato puntual. |

Al subir MAJOR, MINOR vuelve a 0.

## Ejemplos

| Tipo de archivo | Regla | Nombre correcto |
|-----------------|-------|-----------------|
| Plan SCM versión 1, revisión 2 | RN-01 | `Plan_Configuracion_v1.2.md` |
| Minuta de TIG del 5 de sep. | RN-02 | `minuta_2026-09-05.md` |
| Anotación de clase sobre Kanban | RN-02 | `anotacion_2026-10-14_kanban.md` |
| Entregable del TP5 | RN-03 | `tp5_isw_4k2_grupo6.pdf` |
| Slide de la cátedra | RN-04 | `01 SCM.pdf` (nombre original) |
| Resumen de Unidad 3 sobre SCM | RN-05 | `resumen_unidad3_scm.md` |
| Modelo de primer parcial | RN-05 | `modelo_parcial1_2024.pdf` |
| Convenciones de commits | RN-05 | `convenciones_commits.md` |
| Workflow de CI | RN-06 | `telegram-pr-notification.yml` |
