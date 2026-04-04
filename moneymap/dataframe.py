"""
moneymap.dataframe
~~~~~~~~~~~~~~~~~~
Accessor de pandas para MoneyMap.

Registra el accessor `moneymap` en pandas DataFrame, permitiendo
operaciones financieras directamente sobre columnas de montos.

Uso:
    import pandas as pd
    import moneymap.dataframe  # registra el accessor

    df.moneymap.convertir(col="precio", origen="MXN", destino="USD")
    df.moneymap.impuesto(col="precio", pais="Mexico")
    df.moneymap.total_con_impuesto(col="precio", pais="Mexico")
"""

from __future__ import annotations

from decimal import Decimal
from typing import Union

import pandas as pd

from .currency import convertir as _convertir, _TASAS_BASE
from .taxes import (
    impuesto as _impuesto,
    total_con_impuesto as _total_con_impuesto,
    tasa_fiscal as _tasa_fiscal,
    _IMPUESTOS,
)
from .exceptions import DivisaNoSoportadaError, PaisNoSoportadoError


@pd.api.extensions.register_dataframe_accessor("moneymap")
class MoneyMapAccessor:
    """
    Accessor `moneymap` para pandas DataFrame.

    Se activa automáticamente al importar `moneymap.dataframe`.
    Todas las operaciones son no destructivas: agregan columnas nuevas
    sin modificar las columnas originales del DataFrame.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df

    # ── utilidades internas ──────────────────────────────────────────────

    def _validar_columna(self, col: str) -> None:
        if col not in self._df.columns:
            raise KeyError(
                f"La columna '{col}' no existe en el DataFrame. "
                f"Columnas disponibles: {list(self._df.columns)}"
            )

    def _nombre_salida(self, base: str, sufijo: str) -> str:
        """Genera un nombre de columna que no colisione con las existentes."""
        nombre = f"{base}_{sufijo}"
        if nombre in self._df.columns:
            i = 2
            while f"{nombre}_{i}" in self._df.columns:
                i += 1
            nombre = f"{nombre}_{i}"
        return nombre

    # ── métodos públicos ─────────────────────────────────────────────────

    def convertir(
        self,
        col: str,
        origen: str,
        destino: str,
        *,
        resultado: str | None = None,
    ) -> pd.DataFrame:
        """
        Convierte una columna de montos de una divisa a otra.

        Agrega una columna nueva con el nombre `{col}_{destino}` (o el
        nombre indicado en `resultado`) y devuelve el DataFrame completo.

        Args:
            col:       Nombre de la columna con los montos a convertir.
            origen:    Código ISO de la divisa de origen (ej. "MXN").
            destino:   Código ISO de la divisa de destino (ej. "USD").
            resultado: Nombre opcional para la columna de salida.

        Returns:
            DataFrame original con la columna de conversión agregada.

        Raises:
            KeyError:              Si la columna no existe.
            DivisaNoSoportadaError: Si alguna divisa no está registrada.

        Ejemplo:
            >>> df.moneymap.convertir(col="precio", origen="MXN", destino="USD")
            # Agrega columna "precio_USD"
        """
        self._validar_columna(col)

        origen  = origen.upper()
        destino = destino.upper()

        if origen not in _TASAS_BASE:
            raise DivisaNoSoportadaError(origen)
        if destino not in _TASAS_BASE:
            raise DivisaNoSoportadaError(destino)

        nombre_col = resultado or self._nombre_salida(col, destino)

        df = self._df.copy()
        df[nombre_col] = df[col].apply(
            lambda v: float(_convertir(v, origen, destino))
            if pd.notna(v) else None
        )
        return df

    def impuesto(
        self,
        col: str,
        pais: str,
        *,
        resultado: str | None = None,
    ) -> pd.DataFrame:
        """
        Calcula el impuesto (IVA/VAT/GST) de una columna de montos.

        Agrega una columna nueva con el nombre `{col}_impuesto` (o el
        nombre indicado en `resultado`) y devuelve el DataFrame completo.

        Args:
            col:       Nombre de la columna con los montos base.
            pais:      País cuya tasa fiscal se aplicará (ej. "Mexico").
            resultado: Nombre opcional para la columna de salida.

        Returns:
            DataFrame original con la columna de impuesto agregada.

        Raises:
            KeyError:            Si la columna no existe.
            PaisNoSoportadoError: Si el país no tiene reglas fiscales.

        Ejemplo:
            >>> df.moneymap.impuesto(col="precio", pais="Mexico")
            # Agrega columna "precio_impuesto"
        """
        self._validar_columna(col)

        if pais not in _IMPUESTOS:
            raise PaisNoSoportadoError(pais)

        nombre_col = resultado or self._nombre_salida(col, "impuesto")

        df = self._df.copy()
        df[nombre_col] = df[col].apply(
            lambda v: float(_impuesto(v, pais))
            if pd.notna(v) else None
        )
        return df

    def total_con_impuesto(
        self,
        col: str,
        pais: str,
        *,
        resultado: str | None = None,
    ) -> pd.DataFrame:
        """
        Calcula el total (monto base + impuesto) de una columna de montos.

        Agrega una columna nueva con el nombre `{col}_total` y devuelve
        el DataFrame completo.

        Args:
            col:       Nombre de la columna con los montos base.
            pais:      País cuya tasa fiscal se aplicará.
            resultado: Nombre opcional para la columna de salida.

        Returns:
            DataFrame original con la columna de total agregada.

        Ejemplo:
            >>> df.moneymap.total_con_impuesto(col="precio", pais="Mexico")
            # Agrega columna "precio_total"
        """
        self._validar_columna(col)

        if pais not in _IMPUESTOS:
            raise PaisNoSoportadoError(pais)

        nombre_col = resultado or self._nombre_salida(col, "total")

        df = self._df.copy()
        df[nombre_col] = df[col].apply(
            lambda v: float(_total_con_impuesto(v, pais))
            if pd.notna(v) else None
        )
        return df

    def resumen_fiscal(self, col: str, pais: str) -> pd.DataFrame:
        """
        Agrega de una vez tres columnas: impuesto, total y tasa usada.

        Equivale a llamar impuesto() y total_con_impuesto() juntos,
        más una columna informativa con el porcentaje aplicado.

        Args:
            col:  Nombre de la columna con los montos base.
            pais: País cuya tasa fiscal se aplicará.

        Returns:
            DataFrame con tres columnas nuevas:
              - {col}_impuesto
              - {col}_total
              - {col}_tasa_pct

        Ejemplo:
            >>> df.moneymap.resumen_fiscal(col="precio", pais="Mexico")
        """
        self._validar_columna(col)

        if pais not in _IMPUESTOS:
            raise PaisNoSoportadoError(pais)

        tasa = float(_tasa_fiscal(pais))

        df = self._df.copy()
        df[f"{col}_impuesto"] = df[col].apply(
            lambda v: float(_impuesto(v, pais)) if pd.notna(v) else None
        )
        df[f"{col}_total"] = df[col].apply(
            lambda v: float(_total_con_impuesto(v, pais)) if pd.notna(v) else None
        )
        df[f"{col}_tasa_pct"] = tasa
        return df
