"""
moneymap.polars
~~~~~~~~~~~~~~~
Integración de MoneyMap con Polars.

Expone funciones que operan sobre DataFrame, LazyFrame y Expr de Polars.
No usa accessors (Polars no tiene ese sistema) — las funciones reciben
el DataFrame como primer argumento y devuelven uno nuevo.

Modos de uso:

    # 1. DataFrame — agrega columna y devuelve DataFrame nuevo
    import moneymap.polars as mm
    df = mm.convertir(df, col="precio", origen="MXN", destino="USD")

    # 2. LazyFrame — mismo API, evaluación diferida
    lf = mm.convertir(df.lazy(), col="precio", origen="MXN", destino="USD")
    df = lf.collect()

    # 3. Expresión — para usar dentro de .with_columns() o .select()
    df = df.with_columns(
        mm.expr_convertir("precio", origen="MXN", destino="USD").alias("precio_USD")
    )
"""

from __future__ import annotations

from decimal import Decimal
from typing import Union

try:
    import polars as pl
except ImportError as e:
    raise ImportError(
        "polars no está instalado. Ejecuta: pip install moneymap[polars]"
    ) from e

from .currency import convertir as _convertir, _TASAS_BASE
from .taxes import (
    impuesto as _impuesto,
    total_con_impuesto as _total_con_impuesto,
    tasa_fiscal as _tasa_fiscal,
    _IMPUESTOS,
)
from .exceptions import DivisaNoSoportadaError, PaisNoSoportadoError

# Tipo que acepta DataFrame o LazyFrame
FrameType = Union["pl.DataFrame", "pl.LazyFrame"]


# ── utilidades internas ──────────────────────────────────────────────────────

def _validar_divisa(divisa: str) -> None:
    if divisa.upper() not in _TASAS_BASE:
        raise DivisaNoSoportadaError(divisa)


def _validar_pais(pais: str) -> None:
    if pais not in _IMPUESTOS:
        raise PaisNoSoportadoError(pais)


def _nombre_salida(df: "pl.DataFrame | pl.LazyFrame", base: str, sufijo: str) -> str:
    """Genera un nombre de columna que no colisione con las existentes."""
    if isinstance(df, pl.LazyFrame):
        cols = df.columns
    else:
        cols = df.columns
    nombre = f"{base}_{sufijo}"
    if nombre in cols:
        i = 2
        while f"{nombre}_{i}" in cols:
            i += 1
        nombre = f"{nombre}_{i}"
    return nombre


def _aplicar_con_columna(
    df: FrameType,
    col: str,
    nombre_col: str,
    expr: "pl.Expr",
) -> FrameType:
    """Agrega una columna al frame (DataFrame o LazyFrame) y devuelve el mismo tipo."""
    return df.with_columns(expr.alias(nombre_col))


# ── funciones de DataFrame / LazyFrame ──────────────────────────────────────

def convertir(
    df: FrameType,
    col: str,
    origen: str,
    destino: str,
    *,
    resultado: str | None = None,
) -> FrameType:
    """
    Convierte una columna de montos de una divisa a otra.

    Agrega una columna nueva `{col}_{DESTINO}` (o el nombre indicado en
    `resultado`) y devuelve el mismo tipo recibido (DataFrame o LazyFrame).

    Args:
        df:        DataFrame o LazyFrame de Polars.
        col:       Nombre de la columna con los montos a convertir.
        origen:    Código ISO de la divisa de origen (ej. "MXN").
        destino:   Código ISO de la divisa de destino (ej. "USD").
        resultado: Nombre opcional para la columna de salida.

    Returns:
        DataFrame o LazyFrame con la columna de conversión agregada.

    Ejemplo:
        >>> import moneymap.polars as mm
        >>> df = mm.convertir(df, col="precio", origen="MXN", destino="USD")
        >>> lf = mm.convertir(df.lazy(), col="precio", origen="MXN", destino="USD")
    """
    origen  = origen.upper()
    destino = destino.upper()
    _validar_divisa(origen)
    _validar_divisa(destino)

    nombre_col = resultado or _nombre_salida(df, col, destino)
    factor = float(_TASAS_BASE[destino]) / float(_TASAS_BASE[origen])

    expr = (pl.col(col).cast(pl.Float64) * factor).round(2)
    return _aplicar_con_columna(df, col, nombre_col, expr)


def impuesto(
    df: FrameType,
    col: str,
    pais: str,
    *,
    resultado: str | None = None,
) -> FrameType:
    """
    Calcula el impuesto (IVA/VAT/GST) de una columna de montos.

    Agrega una columna nueva `{col}_impuesto` y devuelve el mismo tipo
    recibido (DataFrame o LazyFrame).

    Args:
        df:        DataFrame o LazyFrame de Polars.
        col:       Nombre de la columna con los montos base.
        pais:      País cuya tasa fiscal se aplicará (ej. "Mexico").
        resultado: Nombre opcional para la columna de salida.

    Returns:
        DataFrame o LazyFrame con la columna de impuesto agregada.

    Ejemplo:
        >>> import moneymap.polars as mm
        >>> df = mm.impuesto(df, col="precio", pais="Mexico")
    """
    _validar_pais(pais)
    nombre_col = resultado or _nombre_salida(df, col, "impuesto")
    tasa = float(_IMPUESTOS[pais]) / 100

    expr = (pl.col(col).cast(pl.Float64) * tasa).round(2)
    return _aplicar_con_columna(df, col, nombre_col, expr)


def total_con_impuesto(
    df: FrameType,
    col: str,
    pais: str,
    *,
    resultado: str | None = None,
) -> FrameType:
    """
    Calcula el total (monto base + impuesto) de una columna de montos.

    Agrega una columna nueva `{col}_total` y devuelve el mismo tipo
    recibido (DataFrame o LazyFrame).

    Args:
        df:        DataFrame o LazyFrame de Polars.
        col:       Nombre de la columna con los montos base.
        pais:      País cuya tasa fiscal se aplicará.
        resultado: Nombre opcional para la columna de salida.

    Returns:
        DataFrame o LazyFrame con la columna de total agregada.

    Ejemplo:
        >>> import moneymap.polars as mm
        >>> df = mm.total_con_impuesto(df, col="precio", pais="Mexico")
    """
    _validar_pais(pais)
    nombre_col = resultado or _nombre_salida(df, col, "total")
    tasa = float(_IMPUESTOS[pais]) / 100

    expr = (pl.col(col).cast(pl.Float64) * (1 + tasa)).round(2)
    return _aplicar_con_columna(df, col, nombre_col, expr)


def resumen_fiscal(
    df: FrameType,
    col: str,
    pais: str,
) -> FrameType:
    """
    Agrega de una vez tres columnas: impuesto, total y tasa aplicada.

    Args:
        df:   DataFrame o LazyFrame de Polars.
        col:  Nombre de la columna con los montos base.
        pais: País cuya tasa fiscal se aplicará.

    Returns:
        DataFrame o LazyFrame con tres columnas nuevas:
          - {col}_impuesto
          - {col}_total
          - {col}_tasa_pct

    Ejemplo:
        >>> import moneymap.polars as mm
        >>> df = mm.resumen_fiscal(df, col="precio", pais="España")
    """
    _validar_pais(pais)
    tasa_pct = float(_IMPUESTOS[pais])
    tasa     = tasa_pct / 100

    return df.with_columns([
        (pl.col(col).cast(pl.Float64) * tasa).round(2).alias(f"{col}_impuesto"),
        (pl.col(col).cast(pl.Float64) * (1 + tasa)).round(2).alias(f"{col}_total"),
        pl.lit(tasa_pct).alias(f"{col}_tasa_pct"),
    ])


# ── expresiones (para usar dentro de .with_columns / .select) ───────────────

def expr_convertir(
    col: str,
    origen: str,
    destino: str,
) -> "pl.Expr":
    """
    Devuelve una expresión Polars para convertir una columna de divisas.

    Diseñada para usarse dentro de `.with_columns()` o `.select()`.

    Args:
        col:     Nombre de la columna con los montos.
        origen:  Código ISO de la divisa de origen.
        destino: Código ISO de la divisa de destino.

    Returns:
        pl.Expr — expresión lista para encadenar con .alias().

    Ejemplo:
        >>> import moneymap.polars as mm
        >>> df = df.with_columns(
        ...     mm.expr_convertir("precio", "MXN", "USD").alias("precio_USD"),
        ...     mm.expr_convertir("precio", "MXN", "EUR").alias("precio_EUR"),
        ... )
    """
    origen  = origen.upper()
    destino = destino.upper()
    _validar_divisa(origen)
    _validar_divisa(destino)

    factor = float(_TASAS_BASE[destino]) / float(_TASAS_BASE[origen])
    return (pl.col(col).cast(pl.Float64) * factor).round(2)


def expr_impuesto(col: str, pais: str) -> "pl.Expr":
    """
    Devuelve una expresión Polars para calcular el impuesto de una columna.

    Args:
        col:  Nombre de la columna con los montos base.
        pais: País cuya tasa fiscal se aplicará.

    Returns:
        pl.Expr — expresión lista para encadenar con .alias().

    Ejemplo:
        >>> import moneymap.polars as mm
        >>> df = df.with_columns(
        ...     mm.expr_impuesto("precio", "Mexico").alias("iva"),
        ... )
    """
    _validar_pais(pais)
    tasa = float(_IMPUESTOS[pais]) / 100
    return (pl.col(col).cast(pl.Float64) * tasa).round(2)


def expr_total_con_impuesto(col: str, pais: str) -> "pl.Expr":
    """
    Devuelve una expresión Polars para calcular el total (base + impuesto).

    Args:
        col:  Nombre de la columna con los montos base.
        pais: País cuya tasa fiscal se aplicará.

    Returns:
        pl.Expr — expresión lista para encadenar con .alias().

    Ejemplo:
        >>> import moneymap.polars as mm
        >>> df = df.with_columns(
        ...     mm.expr_total_con_impuesto("precio", "Mexico").alias("precio_total"),
        ... )
    """
    _validar_pais(pais)
    tasa = float(_IMPUESTOS[pais]) / 100
    return (pl.col(col).cast(pl.Float64) * (1 + tasa)).round(2)
