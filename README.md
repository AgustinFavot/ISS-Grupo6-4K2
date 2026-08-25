# ISS-Grupo6-4K2
Ingeniería y Calidad de Software

**Índice del repositorio**

README.md
# propósito del proyecto y guía del repo

00_Configuración/
   - Plan_Configuración_v1.0.md
   - Estándares/
      - convenciones-nombres.md 
      - convenciones-commits.md 
      - convenciones-ramas.md
   - Configuración_Extra/
   # Documento maestro de SCM; versionado por ser línea base en sí mismo
   # Convenciones en lenguaje natural, para lectura humana
   # Regla de nombrado de archivos y carpetas
   # Formato acordado para mensajes de commit
   # Criterio de creación y nombrado de ramas
   # Reservada para ítems futuros (e.g., imágenes de config de ramas, config de bots de cambios)

.gitignore
   # Define qué no se versiona

.github/
   workflows/
      naming-check.yml
   config/
      naming-rules.yml
      branch-rules.yml
   # Automatizaciones de CI
   # Valida nombrado y ramas en cada push/PR
   # Centraliza reglas que los workflows van a leer (YAML)
   # Reglas de nombrado de archivos
   # Reglas de ramas

01_Administrativo/
   Integrantes.md
   Roles.md
   # Gestión del equipo
   # Datos de contacto de cada integrante
   # Rol de cada integrante en el equipo

02_TP/
   GuiaTP_Evaluables.pdf
   TIG/
      TIG_[nro]_[Nombre]/
         Minutas/
   TPG/
      TPG_[nro]_[Nombre]/
         Minutas/
   # Productos evaluables del cursado
   # Consigna original, conservada como referencia
   # Una carpeta por Trabajo de Investigación Grupal
   # Historial de avance de esa entrega
   # Una carpeta por Trabajo Práctico Grupal

03_Material_Estudio/
   Casos_Estudio/
      Casos_Estudio_Resueltos.pdf
      Casos_Estudio_Intensivo.pdf
   Modelos_Evaluación/
   # Todo lo provisto por la cátedra (no autoría propia)
   # Material de práctica entregado por la cátedra
   # Ejemplos de parcial/final, tomados o no

04_Notas_Equipo/
   Resumenes/
   Anotaciones/
   # Todo lo redactado por el equipo (autoría propia)
   # Contenido ya elaborado y sintetizado
   # Notas de clase más crudas, tomadas al momento

05_Bibliografía/
   Enlaces_Utiles.md
   Material_Externo/
      SCM/
      Ing_Sfw/
   # Material externo de referencia/consulta
   # Lista curada de recursos web
   # Libros y papers no clasificados por unidad
   # Bibliografía específica de SCM
   # Bibliografía específica de Ingeniería de Software

06_Cátedra/
   Normas_Academica.md
   Cronograma.md
   Condiciones_Promocion.md
   Contacto_Docentes.md
   # Información institucional
   # Condiciones generales fijadas por la cátedra
   # Fechas clave de entregas y exámenes
   # Requisitos para promocionar
   # Vía de contacto con la cátedra
