ARCHIVO BASE A COMPLETAR
# Plan de Gestión de Configuración de Software (SCM)

**Proyecto:** Cursado de Ingeniería y Calidad de Software – 2026  
**Comisión:** 4K2 | **Grupo:** 6  
**Versión:** 1.0 | **Fecha:** 2026-09-06

---

## 1. Propósito y alcance

Este documento define el Plan de Gestión de Configuración de Software (SCM) del Grupo 6 – 4K2. Su objetivo es establecer los mecanismos de identificación, organización, control y seguimiento de todos los Ítems de Configuración (IC) producidos durante el cursado de la materia Ingeniería y Calidad de Software (ISW) 2026.

El plan cubre:
- La identificación y tipificación de los IC del repositorio.
- La estructura de carpetas del repositorio y la ubicación de cada IC.
- Las reglas generales de nombrado aplicables a los IC.
- El esquema de versionado (MAJOR.MINOR) y sus definiciones.
- Los criterios para la creación de líneas base y su justificación.
- Los roles y responsabilidades del equipo de configuración.

Quedan excluidos del control de versiones: credenciales de acceso, archivos binarios de gran tamaño no relacionados con entregas académicas, y archivos temporales del sistema operativo.

---

## 2. Roles y responsabilidades

| Rol | Responsabilidad |
|-----|-----------------|
| **Administrador SCM** | Mantener este plan actualizado, aprobar cambios estructurales al repositorio y crear líneas base. Rol rotativo entre todos los integrantes. |
| **Colaborador** | Crear y modificar ICs siguiendo las reglas definidas en este plan. Todos los integrantes. |

---

## 3. Estructura del repositorio

La estructura siguiente organiza todos los IC del repositorio. Todo archivo presente en el repositorio debe estar definido como IC en la Sección 4. No se admiten ítems sueltos sin clasificación.

> **Regla estructural:** Si una carpeta contiene un único archivo y no se prevén archivos adicionales, no se crea la carpeta; el archivo va directamente en el nivel superior de su sección.

```
ISS-Grupo6-4K2/
│
├── README.md                                                           # IC-01
├── .gitignore                                                          # IC-06
│
├── .github/
│   └── workflows/                                                      # IC-07
│
├── 00_Configuración/
│   ├── Plan_Configuracion_v[X].[Y].md                                  # IC-02
│   ├── Matriz_Trazabilidad_v[X].[Y].md                                 # IC-03
│   ├── Estandares/
│   │   ├── convenciones-nombres.md                                     # IC-04a
│   │   ├── convenciones-commits.md                                     # IC-04b
│   │   └── convenciones-ramas.md                                       # IC-04c
│   └── Configuracion_Extra/                                            # IC-05 (libre)
│
├── 01_Administrativo/
│   ├── Integrantes.md                                                  # IC-08
│   └── Roles.md                                                        # IC-09
│
├── 02_TP/
│   ├── GuiaTP_Evaluables.pdf                                           # IC-10
│   ├── ISW_Lineamientos para trabajos de investigación 2026 2C.pdf     # IC-29
│   ├── TIG/
│   │   └── TIG_[nro]_[Nombre]/
│   │       ├── ti[nro]_isw_4k2_grupo6.[ext]                            # IC-11
│   │       ├── (anexos – libre)                                        # IC-12
│   │       └── Minutas/
│   │           └── minuta_AAAA-MM-DD.md                                # IC-13
│   └── TPG/
│       └── TPG_[nro]_[Nombre]/
│           ├── tp[nro]_isw_4k2_grupo6.[ext]                            # IC-14
│           ├── (anexos – libre)                                        # IC-15
│           └── Minutas/
│               └── minuta_AAAA-MM-DD.md                                # IC-16
│
├── 03_Material_Estudio/
│   ├── Casos_Estudio/
│   │   ├── casos_estudio_resueltos.pdf                                 # IC-17
│   │   └── casos_estudio_intensivo.pdf                                 # IC-18
│   ├── Modelos_Evaluacion/
│   │   └── modelo_[tipo]_[tema].pdf                                    # IC-19
│   └── Presentaciones/
│       └── (nombre original de cátedra)                                # IC-20
│
├── 04_Notas_Equipo/
│   ├── Resumenes/
│   │   └── resumen_unidad[nro]_[tema].md                               # IC-21
│   └── Anotaciones/
│       └── anotacion_AAAA-MM-DD_[tema].md                              # IC-22
│
├── 05_Bibliografia/
│   ├── enlaces_utiles.md                                               # IC-23
│   └── Material_Externo/
│       └── (por tema: SCM/, Ing_Sfw/, etc.)                            # IC-24
│
└── 06_Catedra/
    ├── modalidad_academica.md                                          # IC-25
    ├── cronograma.md                                                   # IC-26
    ├── condiciones_promocion.md                                        # IC-27
    └── contacto_docentes.md                                            # IC-28
```

---

## 4. Ítems de Configuración (IC)

### 4.1 Tipos de IC

| Código | Tipo | Descripción |
|--------|------|-------------|
| DOC | Documento de proyecto | Documentos del proceso SCM (planes, matrices) |
| STD | Estándar / Convenio | Convenciones acordadas por el equipo |
| CFG | Configuración de herramienta | Archivos de configuración del repositorio y CI/CD |
| ADM | Documento administrativo | Información del equipo (integrantes, roles) |
| ENT | Entregable académico | Documento final de un TP o TIG |
| ACT | Acta / Minuta | Registro de reunión de trabajo |
| ANX | Anexo | Material de soporte de un TP o TIG |
| MTR | Material de cátedra | Documentos provistos por la cátedra |
| NTS | Notas del equipo | Resúmenes y anotaciones elaborados por el equipo |
| BIB | Bibliografía | Referencias y material externo de estudio |

### 4.2 Tabla de ICs

| ID | Ítem de Configuración | Tipo | Regla de nombrado | Ubicación | Descripción |
|----|----------------------|------|-------------------|-----------|-------------|
| IC-01 | README | DOC | `README.md` (fijo) | `/` | Índice y guía del repositorio |
| IC-02 | Plan de Configuración | DOC | RN-01 | `/00_Configuración/` | Documento maestro del SCM. Este documento. |
| IC-03 | Matriz de Trazabilidad | DOC | RN-01 | `/00_Configuración/` | Trazabilidad entre ICs y entregas del cursado |
| IC-04 | Convenciones del equipo | STD | RN-06 | `/00_Configuración/Estandares/` | Archivos de convenciones (nombres, commits, ramas) |
| IC-05 | Configuración extra | CFG | libre | `/00_Configuración/Configuracion_Extra/` | Capturas de branch protection, .editorconfig, etc. |
| IC-06 | .gitignore | CFG | RN-07 | `/` | Exclusiones del control de versiones |
| IC-07 | Workflow de CI | CFG | RN-07 | `/.github/workflows/` | Automatizaciones de validación continua |
| IC-08 | Listado de integrantes | ADM | `Integrantes.md` (fijo) | `/01_Administrativo/` | Datos de contacto de cada integrante |
| IC-09 | Roles del equipo | ADM | `Roles.md` (fijo) | `/01_Administrativo/` | Rol de cada integrante dentro del grupo |
| IC-10 | Guía de TPs evaluables | MTR | RN-04 | `/02_TP/` | Consigna oficial de la cátedra, conservada como referencia |
| IC-11 | Entregable de TIG | ENT | RN-03 | `/02_TP/TIG/TIG_[nro]_[Nombre]/` | Documento final del Trabajo de Investigación Grupal |
| IC-12 | Anexos de TIG | ANX | libre | `/02_TP/TIG/TIG_[nro]_[Nombre]/` | Material de soporte del TIG (planillas, capturas, etc.) |
| IC-13 | Minuta de TIG | ACT | RN-02 | `/02_TP/TIG/TIG_[nro]_[Nombre]/Minutas/` | Registro de reunión de trabajo del TIG |
| IC-14 | Entregable de TPG | ENT | RN-03 | `/02_TP/TPG/TPG_[nro]_[Nombre]/` | Documento final del Trabajo Práctico Grupal |
| IC-15 | Anexos de TPG | ANX | libre | `/02_TP/TPG/TPG_[nro]_[Nombre]/` | Material de soporte del TPG (capturas, código, etc.) |
| IC-16 | Minuta de TPG | ACT | RN-02 | `/02_TP/TPG/TPG_[nro]_[Nombre]/Minutas/` | Registro de reunión de trabajo del TPG |
| IC-17 | Casos de estudio resueltos | MTR | RN-04 | `/03_Material_Estudio/Casos_Estudio/` | Guía de ejercicios prácticos resueltos de la cátedra |
| IC-18 | Casos de estudio intensivo | MTR | RN-04 | `/03_Material_Estudio/Casos_Estudio/` | Casos para el intensivo provistos por la cátedra |
| IC-19 | Modelos de evaluación | MTR | RN-08 | `/03_Material_Estudio/Modelos_Evaluacion/` | Parciales/finales de referencia tomados o no |
| IC-20 | Presentaciones de clase | MTR | RN-04 | `/03_Material_Estudio/Presentaciones/` | Slides provistos por la cátedra (nombre original) |
| IC-21 | Resúmenes del equipo | NTS | RN-09 | `/04_Notas_Equipo/Resumenes/` | Contenido sintetizado y elaborado por el equipo |
| IC-22 | Anotaciones de clase | NTS | RN-10 | `/04_Notas_Equipo/Anotaciones/` | Notas crudas tomadas durante las clases |
| IC-23 | Enlaces útiles | BIB | `enlaces_utiles.md` (fijo) | `/05_Bibliografia/` | Lista curada de recursos web de referencia |
| IC-24 | Material externo | BIB | RN-05 | `/05_Bibliografia/Material_Externo/` | Libros y papers de terceros, clasificados por tema |
| IC-25 | Modalidad académica | MTR | `modalidad_academica.md` (fijo) | `/06_Catedra/` | Condiciones generales de cursado de la cátedra |
| IC-26 | Cronograma | MTR | `cronograma.md` (fijo) | `/06_Catedra/` | Fechas clave: entregas, parciales y exámenes |
| IC-27 | Condiciones de promoción | MTR | `condiciones_promocion.md` (fijo) | `/06_Catedra/` | Requisitos para promocionar la materia |
| IC-28 | Contacto docentes | ADM | `Contacto profes.png` (fijo) | `/06_Catedra/` | Datos de contacto de los docentes de la comisión |
| IC-29 | Lineamientos del trabajo de investigacion grupal | MTR | RN-04 | `/02_TP/` | Consigna oficial de la cátedra, conservada como referencia |

---

## 5. Reglas generales de nombrado

Las siguientes reglas se aplican por categoría de IC. Cada IC en la Sección 4 referencia la regla correspondiente (RN-XX).

| Regla | Patrón | Descripción |
|-------|--------|-------------|
| **RN-01** | `<nombre>_v<MAJOR>.<MINOR>.md` | **Documentos versionados.** `<nombre>` en snake_case sin mayúsculas ni tildes. |
| **RN-02** | `<tipo>_<AAAA-MM-DD>[_<tema>].md` | **Minutas y anotaciones.** `<tipo>`: `minuta` o `anotacion`. Fecha en formato ISO 8601. |
| **RN-03** | `<tipo><nro>_isw_4k2_grupo6.<ext>` | **Entregables grupales.** `<tipo>`: `ti` (TIG) o `tp` (TPG). `<nro>` alineado con la numeración de la cátedra. |
| **RN-04** | nombre original de la cátedra | **Material de cátedra.** Se conserva el nombre exacto con el que fue provisto. Sin modificaciones. |
| **RN-05** | `<apellido_autor>-<titulo_abreviado>.<ext>` | **Material externo.** Todo en minúsculas, sin tildes ni caracteres especiales. Guiones entre palabras. |
| **RN-06** | `convenciones-<tema>.md` | **Convenciones del equipo.** `<tema>`: `nombres`, `commits`, `ramas`. |
| **RN-07** | según convención de la herramienta | **Configuración técnica.** `.gitignore`, `*.yml`, etc. No se modifica el nombre que la herramienta espera. |
| **RN-08** | `modelo_<tipo>_<tema>.<ext>` | **Modelos de evaluación.** `<tipo>`: `parcial`, `final` o `coloquio`. |
| **RN-09** | `resumen_unidad<nro>_<tema>.md` | **Resúmenes del equipo.** `<nro>` es el número de unidad de la materia; `<tema>` en snake_case. |
| **RN-10** | `anotacion_<AAAA-MM-DD>_<tema>.md` | **Anotaciones de clase.** Fecha primero para que el orden cronológico sea automático. |

### 5.1 Convenciones generales aplicables a todas las reglas

- Los nombres de archivo usan **snake_case** (palabras unidas por `_`) salvo las excepciones indicadas (guiones en RN-05 y RN-06).
- **Sin tildes ni ñ** en nombres de archivo para evitar problemas de codificación.
- Las extensiones van siempre en **minúsculas** (`.md`, `.pdf`, `.docx`, `.yml`).
- Las carpetas siguen el patrón `NN_NombreDescriptivo/` con prefijo numérico de dos dígitos para mantener el orden visual del explorador.

### 5.2 Definición de MAJOR y MINOR (esquema de versionado)

El esquema `v<MAJOR>.<MINOR>` aplica únicamente a los ICs que usan **RN-01**.

| Componente | Cuándo se incrementa | Ejemplos concretos |
|------------|----------------------|--------------------|
| **MAJOR** (ajuste relevante) | Cambios que modifican el fondo, la estructura o el alcance del documento. | Nueva sección agregada; cambio de convención que afecta a múltiples ICs; incorporación de nuevos ICs al plan; reorganización de carpetas. |
| **MINOR** (ajuste menor) | Correcciones o mejoras que no alteran el contenido sustancial. | Correcciones ortográficas o de formato; aclaración de un párrafo existente; actualización de un dato puntual (fecha, nombre). |

> Al incrementar MAJOR, MINOR vuelve a **0**.  
> Ejemplo de secuencia: `v1.0` → `v1.1` (corrección) → `v2.0` (nueva sección) → `v2.1` (ajuste menor).

---

## 6. Líneas base (Baselines)

### 6.1 Definición

Una **línea base** (LB) es un conjunto de ICs revisados, acordados por todo el equipo y fijados como punto de referencia estable. A partir de una LB, los cambios son rastreados de forma controlada: se sabe exactamente qué existía antes del cambio y qué se modificó.

En este repositorio las líneas base se materializan como **tags de Git** con el formato:
```
LB-<NN>_<descripcion-breve>
```
Ejemplo: `LB-01_config-inicial`, `LB-02_entrega-tp5`

### 6.2 Criterios para crear una línea base

| Criterio | Momento | Justificación |
|----------|---------|---------------|
| **C1 – Configuración inicial** | Al concluir la carga inicial del repositorio | El repositorio queda operativo y acordado por todo el equipo. Es el punto de partida del control de cambios; sin esta LB no existe referencia con la que comparar los cambios futuros. |
| **C2 – Entrega de TP/TIG** | Inmediatamente antes de entregar un Trabajo Práctico o de Investigación Grupal | El estado del trabajo fue revisado y acordado por el equipo. Constituye un hito formal evaluable. El tag permite revertir el repositorio si la cátedra solicita correcciones o si se detecta un error posterior. |
| **C3 – Antes de un parcial** | 24 horas antes de cada examen parcial | Congela el material de estudio en el estado acordado previo al examen, garantizando igualdad de condiciones para todos los integrantes. Evita que cambios de último momento introduzcan inconsistencias. |
| **C4 – Cierre del cuatrimestre** | Al finalizar el cursado | Establece el estado final del repositorio, útil como referencia histórica para instancias de recuperación o coloquio. |

### 6.3 Registro de líneas base creadas

| Tag | Criterio aplicado | Fecha | Descripción |
|-----|-------------------|-------|-------------|
| `LB-01_config-inicial` | C1 | 2026-08-XX | Estructura base del repositorio cargada y acordada por el equipo |

*(Se actualiza a medida que se crean nuevas LBs.)*

---

## 7. Procedimientos básicos

### 7.1 Incorporar un nuevo IC

1. Verificar que el IC está definido en la Sección 4. Si no lo está, proponer su inclusión al equipo antes de hacer commit.
2. Aplicar la regla de nombrado que corresponde (ver Sección 5).
3. Ubicar el archivo en la carpeta indicada en la tabla de ICs.
4. Hacer commit con mensaje descriptivo (ver `convenciones-commits.md`).
5. Abrir un Pull Request hacia `main` para revisión del equipo.

### 7.2 Modificar un IC versionado (RN-01)

1. Crear la nueva versión del archivo con el número de versión actualizado.
2. Eliminar la versión anterior del repositorio (no conservar duplicados).
3. El mensaje de commit debe indicar la versión anterior y la nueva.

### 7.3 Crear una línea base

1. Asegurarse de que todos los cambios estén commiteados en `main`.
2. Crear el tag: `git tag -a LB-NN_descripcion -m "Línea base: [descripción]"`
3. Publicar el tag: `git push origin LB-NN_descripcion`
4. Registrar la LB en la tabla 6.3 de este plan e incrementar MINOR del plan.
