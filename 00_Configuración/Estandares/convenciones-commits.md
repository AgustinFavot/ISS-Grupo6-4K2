# Convenciones de Mensajes de Commit

## Formato

```
<tipo>: <descripción breve en imperativo>

[cuerpo opcional: más detalle si es necesario]
```

La primera línea no debe superar los **72 caracteres**.

## Tipos permitidos

| Tipo | Cuándo usarlo |
|------|---------------|
| `add` | Se agrega un IC nuevo al repositorio |
| `update` | Se actualiza el contenido de un IC existente |
| `fix` | Se corrige un error (nombre incorrecto, ubicación equivocada, contenido erróneo) |
| `rename` | Se renombra un archivo o carpeta para cumplir una convención |
| `remove` | Se elimina un IC que ya no corresponde |
| `refactor` | Se reorganiza la estructura sin cambiar el contenido de los ICs |
| `docs` | Se modifica documentación del SCM (este plan, la matriz, etc.) |

## Ejemplos

```
add: incorporar entregable TP5 (SCM Uso de Repositorio)

update: completar convenciones de nombres v1.0

fix: corregir ubicacion de casos de estudio a 03_Material_Estudio/

rename: normalizar archivos de 06_Catedra a snake_case

docs: actualizar tabla de lineas base en Plan_Configuracion_v1.1
```

## Consideraciones

- Escribir siempre en **español**, en modo **imperativo** ("agregar", no "agregué" ni "agrega").
- No terminar la primera línea con punto.
- Si el commit afecta a un IC específico, mencionarlo en la descripción.
- Evitar commits masivos; preferir commits atómicos: un cambio lógico por commit.
