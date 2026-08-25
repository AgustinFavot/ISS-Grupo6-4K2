# Estructura del Repositorio

- **README.md**
  - **#** propósito del proyecto y guía del repo

## 00_Configuración/
- **Plan_Configuración_v1.0.md**
  - **#** Documento maestro de SCM; versionado por ser línea base en sí mismo
- **Matriz_Trazabilidad_v1.0.md**
  - **#** Matriz de trazabilidad de los ítems de configuración del repositorio
- **Estándares/**
  - *convenciones-nombres.md*
    - **#** Convenciones en lenguaje natural, para lectura humana
    - **#** Regla de nombrado de archivos y carpetas
  - *convenciones-commits.md*
    - **#** Formato acordado para mensajes de commit
  - *convenciones-ramas.md*
    - **#** Criterio de creación y nombrado de ramas
- **Configuración_Extra/**
  - **#** Reservada para ítems futuros (e.g., imágenes de config de ramas, config de bots de cambios)

---

## .gitignore
- **#** Define qué no se versiona

---

## .github/
- **workflows/**
  - *naming-check.yml*
    - **#** Automatizaciones de CI
    - **#** Valida nombrado y ramas en cada push/PR
- **config/**
  - *naming-rules.yml*
    - **#** Centraliza reglas que los workflows van a leer (YAML)
    - **#** Reglas de nombrado de archivos
  - *branch-rules.yml*
    - **#** Reglas de ramas

---

## 01_Administrativo/
- *Integrantes.md*
  - **#** Gestión del equipo
  - **#** Datos de contacto de cada integrante
- *Roles.md*
  - **#** Rol de cada integrante en el equipo

---

## 02_TP/
- *GuiaTP_Evaluables.pdf*
  - **#** Productos evaluables del cursado
  - **#** Consigna original, conservada como referencia
- **TIG/**
  - **TIG_[nro]_[Nombre]/**
    - **Minutas/**
      - **#** Una carpeta por Trabajo de Investigación Grupal
      - **#** Historial de avance de esa entrega
- **TPG/**
  - **TPG_[nro]_[Nombre]/**
    - **Minutas/**
      - **#** Una carpeta por Trabajo Práctico Grupal

---

## 03_Material_Estudio/
- **Casos_Estudio/**
  - *Casos_Estudio_Resueltos.pdf*
    - **#** Todo lo provisto por la cátedra (no autoría propia)
    - **#** Material de práctica entregado por la cátedra
  - *Casos_Estudio_Intensivo.pdf*
- **Modelos_Evaluacion/**
  - **#** Ejemplos de parcial/final, tomados o no

---

## 04_Notas_Equipo/
- **Resumenes/**
  - **#** Todo lo redactado por el equipo (autoría propia)
  - **#** Contenido ya elaborado y sintetizado
- **Anotaciones/**
  - **#** Notas de clase más crudas, tomadas al momento

---

## 05_Bibliografía/
- *Enlaces_Utiles.md*
  - **#** Material externo de referencia/consulta
  - **#** Lista curada de recursos web
- **Material_Externo/**
  - **SCM/**
  - **Ing_Sfw/**
  - **Testing_Sfw/**
  - **TDD/**
  - **Agilismo/**
  - **Lean_Kanban/**
  - **#** Libros y papers clasificados por tema y no clasificados

---

## 06_Cátedra/
- *Normas_Académica.md*
  - **#** Información institucional
  - **#** Condiciones generales fijadas por la cátedra
- *Cronograma.md*
  - **#** Fechas clave de entregas y exámenes
- *Condiciones_Promocion.md*
  - **#** Requisitos para promocionar
- *Contacto_Docentes.md*
  - **#** Vía de contacto con la cátedra
