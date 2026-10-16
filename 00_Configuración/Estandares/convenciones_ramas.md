# Convenciones de Ramas

## Ramas permanentes

| Rama | Propósito |
|------|-----------|
| `main` | Estado estable y acordado del repositorio. Aquí se crean las líneas base. |

## Ramas de trabajo (temporales)

Para trabajos de cierta envergadura que requieran revisión antes de integrarse a `main`:

```
<tipo>/<descripcion-breve>
```

| Tipo | Cuándo usarlo |
|------|---------------|
| `feature/` | Incorporación de un conjunto nuevo de ICs (ej. estructura de un TP) |
| `fix/` | Corrección de nombres, ubicaciones o contenido incorrecto |
| `docs/` | Actualización de documentos del SCM (plan, matriz, convenciones) |

### Ejemplos

```
feature/estructura-tp5
feature/agregar-tig2
fix/renombrar-catedra-snake-case
docs/actualizar-plan-v1.1
```

## Reglas generales

- Los nombres de rama usan **kebab-case** (palabras separadas por `-`), todo en minúsculas.
- Las ramas de trabajo se eliminan una vez mergeadas a `main`.
- Todo merge a `main` debe hacerse vía **Pull Request**, con al menos una revisión de otro integrante del grupo.
- **No hacer commits directos a `main`** salvo en la configuración inicial del repositorio.

## Flujo de trabajo

```
main ─────────────────────────────────────────────► (estable)
         │                              ▲
         └─► feature/nueva-entrega ─────┘
                (PR + revisión)
```
