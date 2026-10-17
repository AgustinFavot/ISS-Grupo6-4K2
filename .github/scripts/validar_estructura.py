#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de estructura del repositorio contra el Plan de Configuración.

Verifica tres cosas (Plan de Configuración, Secciones 3, 4 y 5):
 1. Que todo archivo trackeado corresponda a un IC definido — no hay
    "ítems sueltos" (observación #3 de la cátedra en el TP4).
 2. Que los nombres cumplan la regla de nombrado (RN) del IC de su
    ubicación. Las zonas RN-04 (material de cátedra, nombre original)
    y "libre" (anexos, bibliografía) no validan nombre por definición.
 3. Que la Matriz de Trazabilidad no declare "✅ Presente" una ruta
    que no existe en el repositorio.

Uso:  python3 .github/scripts/validar_estructura.py
Sale con código 1 si hay violaciones (pensado para CI).
"""

import glob
import re
import subprocess
import sys

# ---------------------------------------------------------------------------
# Patrones de rutas válidas. Un archivo trackeado debe matchear AL MENOS UNO.
# Cada patrón refleja un IC de la tabla 4.2 del Plan y su regla de nombrado.
# ---------------------------------------------------------------------------
PATRONES_VALIDOS = [
    # Raíz (allowlist)
    (r"^README\.md$", "IC-01"),
    (r"^\.gitignore$", "IC-06 (RN-06)"),
    # Configuración del repositorio
    (r"^\.github/PULL_REQUEST_TEMPLATE\.md$", "IC-35 (RN-06)"),
    (r"^\.github/workflows/[A-Za-z0-9._-]+\.ya?ml$", "IC-07 (RN-06)"),
    (r"^\.github/scripts/[a-z0-9_]+\.py$", "IC-07 (RN-06)"),
    # 00_Configuración
    (r"^00_Configuración/Plan_Configuracion_v\d+\.\d+\.md$", "IC-02 (RN-01)"),
    (r"^00_Configuración/Matriz_Trazabilidad_v\d+\.\d+\.md$", "IC-03 (RN-01)"),
    (r"^00_Configuración/Estandares/convenciones_[a-z0-9_]+\.md$", "IC-04 (RN-05)"),
    (r"^00_Configuración/Configuracion_Extra/.+$", "IC-05 (libre)"),
    # 01_Administrativo (allowlist)
    (r"^01_Administrativo/Integrantes\.md$", "IC-08"),
    (r"^01_Administrativo/Roles\.md$", "IC-09"),
    # 02_TP — material de cátedra en la raíz (RN-04: nombre original)
    (r"^02_TP/[^/]+\.pdf$", "IC-10 / IC-33 (RN-04)"),
    # 02_TP — minutas (RN-02)
    (
        r"^02_TP/(TIG|TPG)/(TIG|TPG)_\d+_[A-Za-z0-9-]+/Minutas/"
        r"minuta_\d{4}-\d{2}-\d{2}(_[a-z0-9_-]+)?\.md$",
        "IC-13 / IC-16 (RN-02)",
    ),
    # 02_TP — entregables (RN-03) y anexos (libre) dentro de la carpeta del TP.
    # Los anexos son de nombre libre, por lo que no se puede exigir RN-03 acá;
    # el entregable en sí se controla en la revisión del PR.
    (r"^02_TP/(TIG|TPG)/(TIG|TPG)_\d+_[A-Za-z0-9-]+/[^/]+$", "IC-11/12/14/15"),
    # 03_Material_Estudio — todo es material de cátedra (RN-04: nombre original)
    (r"^03_Material_Estudio/.+$", "IC-17/18/19/20/29/30/31 (RN-04)"),
    # 04_Notas_Equipo — producción propia, nombres controlados
    (r"^04_Notas_Equipo/Resumenes/resumen_[a-z0-9_-]+\.(md|pdf)$", "IC-21 (RN-05)"),
    (
        r"^04_Notas_Equipo/Anotaciones/"
        r"anotacion_\d{4}-\d{2}-\d{2}(_[a-z0-9_-]+)?\.(md|pdf)$",
        "IC-22 (RN-02)",
    ),
    # 05_Bibliografia
    (r"^05_Bibliografia/enlaces_utiles\.md$", "IC-23"),
    (r"^05_Bibliografia/Material_Externo/.+$", "IC-24 (libre)"),
    # 06_Catedra — .md con nombre fijo + PDFs originales de cátedra
    (
        r"^06_Catedra/(modalidad_academica|cronograma|condiciones_promocion"
        r"|contacto_docentes|faq_isw_2026)\.md$",
        "IC-25/26/27/28/32",
    ),
    (r"^06_Catedra/[^/]+\.pdf$", "IC-34 (RN-04)"),
    # .gitkeep: marcador de carpeta vacía, válido en cualquier ubicación
    (r"(^|/)\.gitkeep$", "estructura (carpeta vacía)"),
]

# Pistas por directorio para que el error diga qué regla se esperaba.
PISTAS = [
    (r"^04_Notas_Equipo/Resumenes/", "resumen_<tema>.md  (RN-05, snake_case sin tildes)"),
    (r"^04_Notas_Equipo/Anotaciones/", "anotacion_AAAA-MM-DD[_tema].md  (RN-02)"),
    (r"/Minutas/", "minuta_AAAA-MM-DD[_tema].md  (RN-02)"),
    (r"^00_Configuración/Estandares/", "convenciones_<tema>.md  (RN-05)"),
    (r"^00_Configuración/", "Plan_Configuracion_vX.Y.md o Matriz_Trazabilidad_vX.Y.md (RN-01)"),
    (r"^06_Catedra/", "uno de los 5 .md fijos del Plan, o un PDF original de cátedra (IC-34)"),
    (r"^01_Administrativo/", "Integrantes.md o Roles.md (nombres fijos)"),
    (r"^$", ""),
]


def archivos_trackeados():
    salida = subprocess.run(
        ["git", "-c", "core.quotepath=false", "ls-files"],
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    return [l for l in salida.stdout.splitlines() if l.strip()]


def validar_estructura(archivos):
    errores = []
    for archivo in archivos:
        if not any(re.search(p, archivo) for p, _ in PATRONES_VALIDOS):
            pista = next((h for d, h in PISTAS if re.search(d, archivo)), None)
            msg = f"  ❌ {archivo}"
            if pista:
                msg += f"\n     → nombre esperado en esta ubicación: {pista}"
            else:
                msg += "\n     → no corresponde a ningún IC del Plan (Sección 4). Clasificarlo o quitarlo."
            errores.append(msg)
    return errores


def validar_matriz(archivos):
    """Toda fila '✅ Presente' de la Matriz con ruta concreta debe existir."""
    candidatas = glob.glob("00_Configuración/Matriz_Trazabilidad_v*.md")
    if not candidatas:
        return ["  ❌ No se encontró la Matriz de Trazabilidad (IC-03)."]

    rutas_existentes = set(archivos)
    errores = []
    with open(candidatas[0], encoding="utf-8") as f:
        for linea in f:
            if "✅" not in linea or "|" not in linea:
                continue
            m = re.search(r"`([^`]+)`", linea)
            if not m:
                continue
            ruta = m.group(1).strip()
            if "[" in ruta:  # placeholder tipo TIG_[nro]
                continue
            if ruta.endswith("/"):
                existe = any(a.startswith(ruta) for a in rutas_existentes)
            else:
                existe = ruta in rutas_existentes
            if not existe:
                errores.append(
                    f"  ❌ La Matriz declara '✅ Presente' pero no existe en el repo: {ruta}"
                )
    return errores


def main():
    # La consola de Windows usa cp1252 y no puede imprimir ✅/❌; en CI es UTF-8.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    archivos = archivos_trackeados()
    errores_estructura = validar_estructura(archivos)
    errores_matriz = validar_matriz(archivos)

    print(f"Archivos trackeados analizados: {len(archivos)}")
    print()

    if errores_estructura:
        print("── Ítems sueltos / nombres inválidos ─────────────────────────")
        print("\n".join(errores_estructura))
        print()
    else:
        print("✅ Estructura: todo archivo corresponde a un IC y cumple su regla de nombrado.")

    if errores_matriz:
        print("── Inconsistencias de la Matriz de Trazabilidad ──────────────")
        print("\n".join(errores_matriz))
        print()
    else:
        print("✅ Matriz: toda ruta declarada 'Presente' existe en el repositorio.")

    if errores_estructura or errores_matriz:
        print()
        print("Referencias: Plan de Configuración (Secciones 3, 4 y 5) y")
        print("00_Configuración/Estandares/convenciones_nombres.md")
        sys.exit(1)


if __name__ == "__main__":
    main()
