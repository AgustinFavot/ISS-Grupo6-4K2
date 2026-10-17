# ISS-Grupo6-4K2

Repositorio del **Grupo 6** – Ingeniería y Calidad de Software 2026, comisión 4K2, UTN FRC.

Centraliza todos los Ítems de Configuración (IC) producidos durante el cursado: documentación SCM, entregas formales, material de estudio, notas del equipo y bibliografía. La gestión del repositorio se rige por el **Plan de Configuración** (ver `00_Configuración/`).

## Estructura del repositorio

| Carpeta | Contenido |
|---------|-----------|
| `00_Configuración/` | Plan de Configuración, Matriz de Trazabilidad y estándares del equipo (convenciones de nombres, commits y ramas) |
| `01_Administrativo/` | Integrantes del grupo y roles asignados |
| `02_TP/` | Entregas formales: guía de TPs evaluables, lineamientos de TIG, y carpetas por TIG/TPG con entregables, anexos y minutas |
| `03_Material_Estudio/` | Casos de estudio, modelos de evaluación, presentaciones de clase y templates provistos por la cátedra |
| `04_Notas_Equipo/` | Producción propia del equipo: resúmenes y anotaciones de clase |
| `05_Bibliografia/` | Enlaces útiles y material externo clasificado por tema (SCM, Ing. de Software, Testing, TDD, Agilismo, Lean-Kanban) |
| `06_Catedra/` | Información institucional: modalidad académica, cronograma, condiciones de promoción, contacto docentes y FAQ |
| `.github/` | Automatizaciones del repositorio: validaciones SCM en cada PR (nombre de rama y título), notificación de PRs a Telegram, y template de PR con checklist SCM |

## Documentos de referencia

- **Plan de Configuración** (`00_Configuración/Plan_Configuracion_v1.0.md`) — fuente de verdad: definición de ICs, reglas de nombrado, esquema de versionado, criterios de línea base y procedimientos.
- **Matriz de Trazabilidad** (`00_Configuración/Matriz_Trazabilidad_v1.0.md`) — estado de cada IC y su trazabilidad con los productos académicos.
- **Convenciones** (`00_Configuración/Estandares/`) — reglas de nombres, commits y ramas.

## Reglas de trabajo

- Todo archivo del repositorio debe estar clasificado como IC en el Plan (Sección 4).
- Los nombres de archivo siguen las reglas RN-01 a RN-06 del Plan (Sección 5).
- Los cambios entran a `main` mediante Pull Request con revisión de otro integrante.
- Las líneas base se marcan como tags de Git con formato `v[MAJOR].[MINOR]`.

## Integrantes

Ver `01_Administrativo/Integrantes.md` y `01_Administrativo/Roles.md`.
