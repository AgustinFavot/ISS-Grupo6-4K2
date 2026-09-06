# Matriz de Trazabilidad de Ítems de Configuración

**Versión:** 1.0 | **Fecha:** 2026-09-06

Esta matriz relaciona cada IC con su estado actual en el repositorio y con los productos académicos que lo requieren o generan.

## Estado de ICs en el repositorio

| ID | Ítem de Configuración | Tipo | Archivo/Carpeta en repo | Estado |
|----|----------------------|------|------------------------|--------|
| IC-01 | README | DOC | `README.md` | ✅ Presente |
| IC-02 | Plan de Configuración | DOC | `00_Configuración/Plan_Configuracion_v1.0.md` | ✅ Presente |
| IC-03 | Matriz de Trazabilidad | DOC | `00_Configuración/Matriz_Trazabilidad_v1.0.md` | ✅ Presente |
| IC-04a | Convenciones de nombres | STD | `00_Configuración/Estandares/convenciones-nombres.md` | ✅ Presente |
| IC-04b | Convenciones de commits | STD | `00_Configuración/Estandares/convenciones-commits.md` | ✅ Presente |
| IC-04c | Convenciones de ramas | STD | `00_Configuración/Estandares/convenciones-ramas.md` | ✅ Presente |
| IC-05 | Configuración extra | CFG | `00_Configuración/Configuracion_Extra/` | ⏳ Carpeta creada, sin contenido aún |
| IC-06 | .gitignore | CFG | `.gitignore` | ⚠️ Pendiente de creación |
| IC-07 | Workflow de CI | CFG | `.github/workflows/telegram-pr-notification.yml` | ✅ Presente |
| IC-08 | Listado de integrantes | ADM | `01_Administrativo/Integrantes.md` | ✅ Presente |
| IC-09 | Roles del equipo | ADM | `01_Administrativo/Roles.md` | ✅ Presente |
| IC-10 | Guía de TPs evaluables | MTR | `02_TP/guiatp_evaluables.pdf` | ⚠️ Pendiente de carga |
| IC-11 | Entregable TIG-1 | ENT | `02_TP/TIG/TIG_1_Despliegue-de-Producto/ti1_isw_4k2_grupo6.pdf` | ⚠️ Pendiente de carga |
| IC-11 | Entregable TIG-2 | ENT | `02_TP/TIG/TIG_2_Frameworks-Lean-Agile/ti2_isw_4k2_grupo6.pdf` | ⚠️ Pendiente de carga |
| IC-12 | Anexos de TIG | ANX | `02_TP/TIG/TIG_[nro]_[Nombre]/` | ⏳ Según avance de cada TIG |
| IC-13 | Minutas de TIG | ACT | `02_TP/TIG/TIG_[nro]_[Nombre]/Minutas/` | ⏳ Según avance de cada TIG |
| IC-14 | Entregable TPG-4 | ENT | `02_TP/TPG/TPG_4_SCM-Herramientas-SCM/tp4_isw_4k2_grupo6.pdf` | ⚠️ Pendiente de carga |
| IC-14 | Entregable TPG-5 | ENT | `02_TP/TPG/TPG_5_SCM-Uso-de-Repositorio/tp5_isw_4k2_grupo6.pdf` | ⏳ En curso (entrega: 17/11/2026) |
| IC-15 | Anexos de TPG | ANX | `02_TP/TPG/TPG_[nro]_[Nombre]/` | ⏳ Según avance de cada TPG |
| IC-16 | Minutas de TPG | ACT | `02_TP/TPG/TPG_[nro]_[Nombre]/Minutas/` | ⏳ Según avance de cada TPG |
| IC-17 | Casos de estudio resueltos | MTR | `03_Material_Estudio/Casos_Estudio/` | ⚠️ Pendiente de carga |
| IC-18 | Casos de estudio intensivo | MTR | `03_Material_Estudio/Casos_Estudio/` | ⚠️ Pendiente de carga |
| IC-19 | Modelos de evaluación | MTR | `03_Material_Estudio/Modelos_Evaluacion/` | ⏳ Disponibles tras cada parcial |
| IC-20 | Presentaciones de clase | MTR | `03_Material_Estudio/Presentaciones/` | ⚠️ Pendiente de carga |
| IC-21 | Resúmenes del equipo | NTS | `04_Notas_Equipo/Resumenes/` | ⏳ Según avance del cursado |
| IC-22 | Anotaciones de clase | NTS | `04_Notas_Equipo/Anotaciones/` | ⏳ Según avance del cursado |
| IC-23 | Enlaces útiles | BIB | `05_Bibliografia/enlaces_utiles.md` | ✅ Presente |
| IC-24 | Material externo | BIB | `05_Bibliografia/Material_Externo/` | ⏳ Según incorporación de bibliografía |
| IC-25 | Modalidad académica | MTR | `06_Catedra/modalidad_academica.md` | ✅ Presente |
| IC-26 | Cronograma | MTR | `06_Catedra/cronograma.md` | ✅ Presente |
| IC-27 | Condiciones de promoción | MTR | `06_Catedra/condiciones_promocion.md` | ✅ Presente |
| IC-28 | Contacto docentes | ADM | `06_Catedra/contacto_docentes.md` | ✅ Presente |

**Leyenda:**  
✅ Presente y completo | ⏳ Pendiente según avance | ⚠️ Pendiente de acción inmediata

## Trazabilidad IC ↔ Producto académico

| ID | Ítem de Configuración | TP/TIG que lo genera o requiere | Unidad temática |
|----|----------------------|---------------------------------|-----------------|
| IC-02 | Plan de Configuración | TPG-5 (SCM Uso de Repositorio) | Unidad 3 – SCM |
| IC-03 | Matriz de Trazabilidad | TPG-5 (SCM Uso de Repositorio) | Unidad 3 – SCM |
| IC-04 | Convenciones del equipo | TPG-5 (SCM Uso de Repositorio) | Unidad 3 – SCM |
| IC-10 | Guía de TPs evaluables | Todos los TPGs | General |
| IC-11 | Entregable TIG | TIG-1, TIG-2 | Unidades 1–4 |
| IC-13 | Minutas de TIG | TIG-1, TIG-2 | Unidades 1–4 |
| IC-14 | Entregable TPG | TPG-4, TPG-5, TPG-6, TPG-7, TPG-9, TPG-11, TPG-12 | Unidades 1–4 |
| IC-16 | Minutas de TPG | Todos los TPGs | General |
| IC-17 | Casos de estudio resueltos | Preparación de parciales | Unidades 1–4 |
| IC-19 | Modelos de evaluación | Preparación de parciales | Unidades 1–4 |
| IC-20 | Presentaciones de clase | Material de estudio | Unidades 1–4 |
| IC-21 | Resúmenes del equipo | Material de estudio | Unidades 1–4 |
